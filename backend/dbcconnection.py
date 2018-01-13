"""
Class for mongodb database and collection Connection details.

@author : Ludvig Olsen
@date   : Dec, 2017
"""

__all__ = ["DBCConnection"]


class DBCConnection(object):
    """Class for instantiating connection details for mongodb collection in database."""

    def __init__(self, host="127.0.0.1", port="27017", username=None,
                 password=None, db=None, collection=None,
                 out_dir="out/", pretty_name="Tweets", called_by="Tweets",
                 max_count=None):
        super(DBCConnection, self).__init__()

        self.check_input_str(host, "host")
        self.check_input_str(port, "port")
        if username:
            self.check_input_str(username, "username")
        if password:
            self.check_input_str(password, "password")
        if not db:
            raise ValueError("db must be str with name of database")
        self.check_input_str(db, "db")
        if not collection:
            raise ValueError("collection must be str with name of collection")
        self.check_input_str(collection, "collection")
        self.check_input_str(out_dir, "out_dir")
        self.check_input_str(pretty_name, "pretty_name")
        self.check_input_str(called_by, "called_by")
        if max_count and not isinstance(max_count, int):
            raise ValueError("max_count must be int or None.")

        self.host_ = host
        self.port_ = port
        self.username_ = username
        self.password_ = password
        self.db_ = db
        self.collection_ = collection
        self.out_dir_ = out_dir
        self.pretty_name_ = pretty_name
        self.called_by_ = called_by
        self.max_count_ = max_count

    @property
    def host(self):
        return self.host_

    @property
    def port(self):
        return self.port_

    @property
    def username(self):
        return self.username_

    @property
    def password(self):
        return self.password_

    @property
    def db(self):
        return self.db_

    @property
    def collection(self):
        return self.collection_

    @property
    def out_dir(self):
        return self.out_dir_

    @property
    def pretty_name(self):
        return self.pretty_name_

    @property
    def called_by(self):
        return self.called_by_

    @property
    def max_count(self):
        return self.max_count_

    def check_input_str(self, s, arg_name):
        """
        Checks that argument s is a string.
        :param s: str.
        :param arg_name: name of argument to include in error message.
        """
        if not isinstance(s, str):
            raise ValueError("{} should be a string.".format(arg_name))
