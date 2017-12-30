"""
Runs the streamer.

@author: Ludvig Olsen
"""

import re
import time
from http.client import IncompleteRead

import tweepy

from backend.email_me_error import email_me_error

__all__ = ["run_streamer"]


def run_streamer(tw_connection, listener, WORDS, LANGUAGES, sleep_time=15, mail_connection=None):
    while True:
        try:
            # Connect/reconnect the stream
            streamer = tweepy.Stream(auth=tw_connection.auth, listener=listener)
            print("Tracking: " + str(WORDS))

            streamer.filter(track=WORDS, languages=LANGUAGES, async=False)
        except IncompleteRead:
            # Ignore this exception
            continue
        except KeyboardInterrupt:
            # If user interrupts, disconnect stream and break out!
            streamer.disconnect()
            break
        except BaseException as e:
            # If it's still the IncompleteRead error
            # that for some reason wasn't captured before
            # continue running the script
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
