"""
Class for creating twitter API Connection.

@author : Ludvig Olsen
@date   : Dec, 2017
"""

import tweepy

__all__ = ["TWConnection"]


class TWConnection(object):
    """Class for creating twitter API Connection."""

    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret):
        """
        Create Connection object.

        To get consumer keys and access tokens, you will need to create a twitter application.
        See: http://apps.twitter.com/

        :param consumer_key: str.
        :param consumer_secret: str.
        :param access_token: str.
        :param access_token_secret: str.
        """
        super(TWConnection, self).__init__()

        self.check_input_str(consumer_key, "consumer_key")
        self.check_input_str(consumer_secret, "consumer_secret")
        self.check_input_str(access_token, "access_token")
        self.check_input_str(access_token_secret, "access_token_secret")

        self.consumer_key_ = consumer_key
        self.consumer_secret_ = consumer_secret
        self.access_token_ = access_token
        self.access_token_secret_ = access_token_secret

        self.setup_auth()

    def setup_auth(self):
        """ set up authorization and api access"""
        auth = tweepy.OAuthHandler(self.consumer_key_, self.consumer_secret_)
        auth.set_access_token(self.access_token_, self.access_token_secret_)
        self.auth_ = auth

    @property
    def consumer_key(self):
        return self.consumer_key_

    @property
    def consumer_secret(self):
        return self.consumer_secret_

    @property
    def access_token(self):
        return self.access_token_

    @property
    def access_token_secret(self):
        return self.access_token_secret_

    @property
    def auth(self):
        if self.auth_:
            return self.auth_
        else:
            raise ValueError("auth is None.")

    def check_input_str(self, s, arg_name):
        """
        Checks that argument s is a string.
        :param s: str.
        :param arg_name: name of argument to include in error message.
        """
        if not isinstance(s, str):
            raise ValueError("{} should be a string.".format(arg_name))
