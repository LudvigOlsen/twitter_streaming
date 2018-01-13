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


def run_streamer(tw_connection, listener, WORDS, LANGUAGES, sleep_time=15, mail_connection=None, sleep_every_24h=False):

    t1 = time.time()
    while True:
        try:
            # Connect/reconnect the stream
            streamer = tweepy.Stream(auth=tw_connection.auth, listener=listener)
            print("Tracking: " + str(WORDS))

            streamer.filter(track=WORDS, languages=LANGUAGES, async=False)
        except IncompleteRead:
            # Ignore this exception
            if sleep_every_24h:
                t1 = sleep_if(streamer, t1)
            continue
        except AttributeError as e:
            if sleep_every_24h:
                t1 = sleep_if(streamer, t1)
            if bool(re.search('has no attribute', str(e))):
                continue
        except KeyboardInterrupt:
            # If user interrupts, disconnect stream and break out!
            streamer.disconnect()
            break
        except BaseException as e:
            # If it's still the IncompleteRead error
            # that for some reason wasn't captured before
            # continue running the script
            if sleep_every_24h:
                t1 = sleep_if(streamer, t1)
            if bool(re.search('IncompleteRead', str(e))):
                continue
            else:
                try:
                    e_ = "\r\n".join(
                        [str(e), "Will sleep {} minutes and try to continue afterwards".format(sleep_time)])
                    if mail_connection:
                        email_me_error("unknown", custom_msg=e_)
                    else:
                        print(e_)
                    streamer.disconnect()
                    time.sleep(sleep_time)
                    continue
                except:
                    e_ = "\r\n".join([str(e), "Failed to continue. Please take action."])
                    if mail_connection:
                        email_me_error("unknown", custom_msg=e_)
                    else:
                        print(e_)
                    streamer.disconnect()
                    print(str(e))
                    break


def sleep_if(streamer, t1):
    if (time.time()-t1)//(60*60) > 60*60*24:
        try:
            streamer.disconnect()  
        except:
            pass
        print("Will sleep for 48 hours")
        time.sleep(60*60*48)
        return time.time()

