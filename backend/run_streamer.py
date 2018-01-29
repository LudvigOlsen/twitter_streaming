"""
Runs the streamer.

This version of the script runs for 24 hours, then sleeps for 48 hours, and resumes. 
NOTE: It only checks the time when exceptions are raised though. Otherwise I would need to run async.

@author: Ludvig Olsen
"""

import re
import time
from http.client import IncompleteRead

import tweepy

from backend.email_me_error import email_me_error

__all__ = ["run_streamer"]


def run_streamer(tw_connection, listener, WORDS, LANGUAGES, error_sleep_time=15, mail_connection=None, sleep_every=None,
                 sleep_for=None):
    """
    Runs the twitter streamer.
    If sleep_every and sleep_for are integers (hours), the script will check whenever an exception is raised, whether
    it's been sleep_every hours since the last streaming break, and disconnect the stream, sleep for sleep_for hours,
    and then resume streaming. This approach has been chosen, to avoid running asynchronously.

    :param tw_connection: TWConnection object.
    :param listener: StreamListener object.
    :param WORDS: The keywords to search for.
    :param LANGUAGES: The languages to fetch.
    :param error_sleep_time: Time to sleep (minutes) on unknown errors.
    :param mail_connection: Dictionary with email details.
    :param sleep_every: How many (hours) to stream before sleeping.
        Useful when wanting to stream over a long period of time (e.g. months) but streaming constantly is too much.
    :param sleep_for: How many (hours) to sleep, when taking a break from streaming.
    :return:
    """

    error_sleep_time = error_sleep_time * 60  # seconds to minutes
    if sleep_every:
        if not sleep_for:
            raise ValueError("sleep_for cannot be None when sleep_every is not None.")
        if not isinstance(sleep_every, int):
            raise TypeError("sleep_every must be int or None.")
        if not isinstance(sleep_for, int):
            raise TypeError("sleep_for must be int.")

    t1 = time.time()

    while True:
        try:
            # Connect/reconnect the stream
            streamer = tweepy.Stream(auth=tw_connection.auth, listener=listener)
            print("Tracking: " + str(WORDS))

            streamer.filter(track=WORDS, languages=LANGUAGES, async=False)
        except IncompleteRead:
            # Ignore this exception
            if sleep_every:
                t1 = sleep_if(streamer, t1, sleep_every, sleep_for)
            continue
        except AttributeError as e:
            if sleep_every:
                t1 = sleep_if(streamer, t1, sleep_every, sleep_for)
            if bool(re.search("has no attribute", str(e))):
                continue
        except KeyboardInterrupt:
            # If user interrupts, disconnect stream and break out!
            streamer.disconnect()
            break
        except BaseException as e:
            # If it's still the IncompleteRead error
            # that for some reason wasn't captured before
            # continue running the script
            if sleep_every:
                t1 = sleep_if(streamer, t1, sleep_every, sleep_for)
            if bool(re.search('IncompleteRead', str(e))):
                continue
            else:
                try:
                    e_ = "\r\n".join(
                        [str(e), "Will sleep {} minutes and try to continue afterwards".format(error_sleep_time)])
                    if mail_connection:
                        error_mail_wrapper(mail_connection=mail_connection, status_code="unknown", 
                                           custom_msg=e_, streamer=streamer, sleep_time=error_sleep_time)
                    else:
                        print(e_)
                    try:
                        streamer.disconnect()
                    except:
                        pass
                    time.sleep(error_sleep_time)
                    continue
                except:
                    e_ = "\r\n".join([str(e), "Failed to continue. Please take action."])
                    if mail_connection:
                        error_mail_wrapper(mail_connection=mail_connection, status_code="unknown", 
                                           custom_msg=e_, streamer=streamer, sleep_time=error_sleep_time)
                    else:
                        print(e_)
                    try:
                        streamer.disconnect()
                    except:
                        pass
                    print(str(e))
                    break


def sleep_if(streamer, t1, sleep_every, sleep_for):
    if int((time.time() - t1) / (60 * 60)) > int(60 * 60 * sleep_every):
        try:
            streamer.disconnect()
        except:
            pass
        print("Will sleep for {} hours".format(sleep_for))
        time.sleep(60 * 60 * sleep_for)
        return time.time()

def error_mail_wrapper(mail_connection, status_code, custom_message, streamer, sleep_time):
    while True:
        # Until email is sent, disconnect, sleep, attempt again
        try:
            email_me_error(mail_connection, status_code, custom_msg)
            return False
        except:
            try:
                streamer.disconnect()
            except:
                pass
            print("Could not send email")
            time.sleep(sleep_time)
