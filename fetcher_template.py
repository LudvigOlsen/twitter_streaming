import tweepy
from pymongo import MongoClient

from stream_listener import StreamListener
from twconnection import TWConnection
from dbcconnection import DBCConnection
from run_streamer import run_streamer

"""
Assumes you have mongodb installed locally
and that you have a database called "test"
"""
MONGO_HOST = 'mongodb://localhost/test'

""" 
Database (mongodb) information.

Has not been tested with a database requiring username and password.

pretty_name is used in error emails.

If max_count is an integer, the collection will be dumped to disk and cleared for new tweets when that number of 
tweets has been handled by the script. Attempts to get the current number of objects in the collection and 
to start counting from that. 
"""
db_connection = DBCConnection(host="127.0.0.1", port="27017", username=None, password=None,
                              db="test", collection="test_collection", out_dir="out/",
                              pretty_name="Test Tweets", called_by="test, computer 1",
                              max_count=None)

"""
Create twitter connection.

To get consumer keys and access tokens, you will need to create a twitter application.
See: http://apps.twitter.com/

It is recommended to create a twitter account specifically for streaming.
"""
tw_connection = TWConnection(consumer_key="",
                             consumer_secret="",
                             access_token="",
                             access_token_secret="")

"""
Mail account information for emailing when errors occur.
NOTE: Currently only tested with gmail.

It is recommended to create a new gmail account specifically for this purpose,
as the password is hardcoded.

Important: You must make sure that gmail recognizes your device as safe. 
You must also "allow less secure apps" at:
    https://myaccount.google.com/security?pli=1&nlr=1#connectedapps
The latter is another good reason to have a separate gmail account.

Set to None to disable error emails.
"""
mail_connection = {"smtp": "smtp.gmail.com:587",
                   "from": "test@gmail.com",
                   "to": "test@outlook.com",
                   "password": ""}

WORDS = [u"snack", u"humus", u"bitcoin"]

LANGUAGES = ["en"]

if __name__ == '__main__':
    # Set up the listener:
    # The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
    # collect_retweets specifies whether to collect retweets or not.
    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True), db_connection=db_connection,
                              mongo_host=MONGO_HOST, mail_connection=mail_connection, collect_retweets=False)

    run_streamer(tw_connection=tw_connection, listener=listener, WORDS=WORDS, LANGUAGES=LANGUAGES,
                 sleep_time=15, mail_connection=mail_connection)
