# twitter_streaming

A full setup for streaming tweets with tweepy, storing them in mongoDB and sending emails if a non-trivial error occurs. 

# Features
- Search for keywords.  
- Add tweets to mongoDB database.  
- Send mails about non-trivial errors.  
- Sleep for 15 minutes (optional) on non-trivial errors to avoid problems with Twitters rate-limit.  
- Dump collection every n tweets collected and clear collection. Resumes collecting tweets automatically. Uses mongodump. (Not default behaviour)  
- Filter out retweets.  

# Getting started

'$' signals that the following should be typed into the terminal.  
'>' signals that the following should be typed in mongo shell.  

## Installation
First make sure you have installed the dependencies:

### Dependencies
 - python=>3.5  
  - tweepy  
  - pymongo  
 - mongoDB (only local install has been tested)  

### Installing python packages
$ <code>pip install tweepy pymongo</code>   

### Installing mongoDB
https://docs.mongodb.com/manual/administration/install-community/

## Streaming

1. Make a copy of the file “fetcher_template.py” and give it a fitting name (e.g. “politics_fetcher.py” if you’re collecting tweets about politics).

2. Fill out the details in the new file for connecting to your database, twitter application, and gmail. I recommend creating a new twitter account and a new gmail account specifically for collecting tweets.  
You will need to create a twitter application (very easy) at http://apps.twitter.com/ to obtain the needed keys for connecting to the API.  

3. Add your keywords and languages.

4. Run the file in terminal, e.g.:  
$ <code>python politics_fetcher.py</code>  

## Extras
Open a new terminal and type:  
$ <code>mongo</code>    
\> <code>use \<database name\></code>   

### To see how many tweets have been collected, open a new terminal and type:  
\> <code>db.stats()</code>  

### To show the text fields of the first 10 tweets with the pattern 'test':  
\> <code>db.\<collection name\>.find({text:{$regex: 'test', $options:'i'}},{text:1}).limit(10)</code>  

### To count the tweets with the pattern 'test’:  
\> <code>db.\<collection name\>.find({text:{$regex: 'test', $options:'i'}}).count()</code>  

### To dump the database to disk (e.g. for backup):  
In terminal (NOT within mongo shell), type:  
$ <code>mongodump --host \<host\>:\<port\> -d \<database name\> -c \<collection name\> -o \<output directory path\></code>  
e.g.:  
$ <code>mongodump --host 127.0.0.1:27017 -d test_db -c test_collection -o out/</code>    

You might have to create the output directory first.

### To export specific tweets to a csv file:  
In terminal (NOT within mongo shell), type in one line:  
$ <code>mongoexport -h \<host\>:\<port\> -d \<database name\> -c \<collection name\> --type=csv --fields _id,created_at,id,text,source,user.id,user.name,user.screen_name,user.location,user.url,user.description,user.time_zone,user.lang,user.verified,user.created_at,user.followers_count,user.friends_count,user.statuses_count,user.favourites_count,retweeted,lang,timestamp_ms -q '{text:{$regex: "\<search pattern\>", $options:"i"}}' --out test_output.csv</code>  

These are the fields I usually include, but you can choose the fields you need.  

# Notes
I have currently only tested with ubuntu 17.10 and 17.04. It should work on other operating systems as well though. Otherwise, let me know.  