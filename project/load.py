from database import Database
import psycopg2 as pg
from user import User
import oauth2
import constants
import json

#Create a consumer, which uses TW_CONSUMER_KEY and TW_CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.TW_CONSUMER_KEY, constants.TW_CONSUMER_SECRET)     #"""Getting OAuth access token SEC 113"""

email=input("Please Enter Email Account:")
table_name='new_users'
user=User.load_from_db_by_token(email, table_name)

##Why not save these?
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)          #"""Performing Twitter Requests : Getting Images Sec 114"""
authorized_client = oauth2.Client(consumer, authorized_token)               #"""Performing Twitter Requests : Getting Images Sec 114"""

search= input("What to search for?")

response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q={}+filter:images'.format(search),'GET')          #"""Performing Twitter Requests : Getting Images Sec 114"""

if response.status != 200:          #"""Performing Twitter Requests : Getting Images Sec 114"""
    print("An error occurred when searching!")          #"""Performing Twitter Requests : Getting Images Sec 114"""
tweets = json.loads(content.decode('utf-8'))          #"""Performing Twitter Requests : Getting Images Sec 114"""

for tweet in tweets['statuses']:          #"""Performing Twitter Requests : Getting Images Sec 114"""
    print(tweet['text'])          #"""Performing Twitter Requests : Getting Images Sec 114"""
