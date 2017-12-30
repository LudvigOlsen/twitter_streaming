# twitter_streaming

A full setup for streaming tweets with tweepy, storing them in mongoDB and sending emails if a non-trivial error occurs. 

# Features
Search for keywords.  
Add tweets to mongoDB database.  
Send mails about non-trivial errors.  
Sleep for 15 minutes (optional) on non-trivial errors to avoid problems with Twitters rate-limit.  
Dump collection every n tweets collected and clear collection. Resumes collecting tweets automatically. Uses mongodump. (Not default behaviour)  
Filter out retweets.  

# Getting started

## Installation
First make sure you have installed the dependencies:

### Dependencies
python=>3.5  
python packages:  
 - tweepy  
 - pymongo  
mongoDB (only local install has been tested)  

### Installing python packages
$ pip install tweepy pymongo  

Note: ‘$’ signals that the following should be typed into the terminal.  

### Installing mongoDB
https://docs.mongodb.com/manual/administration/install-community/

## Preparing for streaming

1. Make a copy of the file “fetcher_template.py” and give it a fitting name (e.g. “politics_fetcher.py” if you’re collecting tweets about politics).

2. Fill out the details in the new file for connecting to your database, twitter application, and gmail. I recommend creating a new twitter account and a new gmail account specifically for collecting tweets. 

3. Add your keywords and languages.

4. Run the file in terminal, e.g.:  
$ python politics_fetcher.py  

5. To see how many tweets have been collected, open a new terminal and type:
$ mongo  
$ use <database>  
$ db.stats()  


# Notes
I have currently only tested with ubuntu 17.10 and 17.04. It should work on other operating systems as well though. Otherwise, let me know.