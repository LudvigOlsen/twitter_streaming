import tweepy
import json
from pymongo import MongoClient
from backup_db import call_backup
from email_me_error import email_me_error
from dbcconnection import DBCConnection

__all__ = ["StreamListener"]


class StreamListener(tweepy.StreamListener):
    # For accessing the Twitter Streaming API.

    def __init__(self, api=None, db_connection=None, mongo_host=None, mail_connection=None, collect_retweets=False):
        super(StreamListener, self).__init__(api=api)

        if not db_connection:
            raise ValueError("db_connection should be a dictionary.")
        if not isinstance(db_connection, DBCConnection):
            raise ValueError("db_connection should be an instance of DBCConnection.")
        if not mongo_host:
            raise ValueError("mongo_host should be a string.")
        if not isinstance(mongo_host, str):
            raise ValueError("mongo_host should be a string.")
        if not isinstance(collect_retweets, bool):
            raise ValueError("collect_retweets should be a bool.")

        self.db_connection = db_connection
        self.max_count = self.db_connection.max_count
        self.mail_connection = mail_connection
        self.collect_retweets = collect_retweets

        self.client = MongoClient(mongo_host)
        self.db = self.client[self.db_connection.db]
        self.collection_name = self.db_connection.collection

        # Set num_tweets to the number of objects in collection
        if self.max_count:
            self.num_tweets = self.db[self.collection_name].count()

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs
        # display the error / status code
        # Send mail to notify me
        print('An Error has occured: ' + repr(status_code))
        if self.mail_connection and status_code in {420, 500, 502, 503, 504}:
            try:
                email_me_error(self.mail_connection, status_code,
                               custom_msg="--{}--".format(self.db_connection.pretty_name))
            except:
                print("Could not send mail with error message!")
        return False

    def on_data(self, data):
        # Connect to mongoDB and store the tweet
        try:

            if self.max_count:
                if self.num_tweets >= self.max_count:
                    assert self.db[self.collection_name].count() >= self.num_tweets, \
                        "number of tweets added greater than number of tweets in collection"
                    # Backup db
                    call_backup(self.db_connection, self.mail_connection)
                    # Delete db content
                    self.db[self.collection_name].remove({})
                    # Reset num_tweets
                    self.num_tweets = 0

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # If we don't want to collect retweets
            if not self.collect_retweets:
                if "RT" not in datajson['text'][0:2]:
                    self.add_to_collection(datajson=datajson)
                else:
                    print("Skipped retweet!")
            else:
                self.add_to_collection(datajson=datajson)
        except Exception as e:
            print(e)

    def add_to_collection(self, datajson):
        created_at = datajson['created_at']

        # print out a message to the screen that we have collected a tweet
        print("Tweet collected at " + str(created_at))

        # insert the data into the mongoDB into a collection called twitter_search
        # if twitter_search doesn't exist, it will be created.
        self.db[self.collection_name].insert(datajson)

        if self.max_count:
            # Add to tweets counter
            self.num_tweets += 1
