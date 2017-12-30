"""
Dumps given database to disk.
Uses mongodump via subprocess. Sends email on error.

"""

import os
import datetime
import subprocess
from email_me_error import email_me_error

__all__ = ["call_backup"]


def _backup(hostname, port, db, rel_out_dir, username=None, password=None):
    now = datetime.datetime.now()
    output_dir = os.path.abspath(os.path.join(
        os.path.curdir,
        rel_out_dir))

    # If output folder does not exist, create it
    if not os.path.isdir(output_dir):
        print("Creating output folder at {}".format(output_dir))
        try:
            os.mkdir(output_dir)
        except PermissionError as e:
            raise PermissionError("Could not create output folder. {}".format(e))
        except BaseException as e:
            raise EnvironmentError("Could not create output folder. {}".format(e))
    assert os.path.isdir(output_dir), 'Directory %s can\'t be found.' % output_dir

    output_dir = os.path.abspath(os.path.join(output_dir, '%s__%s' % (db, now.strftime('%Y_%m_%d_%H%M%S'))))
    print("Dumping to:", output_dir)

    if username and password:
        _ = subprocess.check_output(
            [
                'mongodump',
                '--host', '%s' % hostname + ":" + port,
                '-u', '%s' % username,
                '-p', '%s' % password,
                '-d', '%s' % db,
                '-o', '%s' % output_dir
            ])
    elif username:
        _ = subprocess.check_output(
            [
                'mongodump',
                '--host', '%s' % hostname + ":" + port,
                '-u', '%s' % username,
                '-d', '%s' % db,
                '-o', '%s' % output_dir
            ])
    else:
        _ = subprocess.check_output(
            [
                'mongodump',
                '--host', '%s' % hostname + ":" + port,
                '-d', '%s' % db,
                '-o', '%s' % output_dir
            ])


def call_backup(db_connection, mail_connection=None):
    try:
        # Dump to disk
        _backup(db_connection.host, db_connection.port,
                db_connection.db, db_connection.out_dir,
                db_connection.username, db_connection.password)
        print("Successfully dumped to disk.")
    except AssertionError as e:
        print("Could not dump db!")
        if mail_connection:
            email_me_error(mail_connection,
                           "dump_error",
                           "{}: There was an assertion error when attempting to dump to disk.".format(
                               db_connection.called_by))
        raise AssertionError("Dump error", e)
    except Exception as e:
        print("Could not dump db!")
        print(e)
        if mail_connection:
            email_me_error(mail_connection,
                           "dump_error",
                           "{}: There was an error when attempting to dump to disk.".format(db_connection.called_by))
        raise Exception("Dump error", e)
