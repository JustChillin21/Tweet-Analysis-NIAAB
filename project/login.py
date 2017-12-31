import constants
import oauth2
import urllib.parse as urlparse
import json
from user import User
from twitter_utils import consumer, get_request_token, get_oauth_verifier, get_access_token
#import urllib.request
#from bs4 import BeautifulSoup
"""The above needed to grab info from web pages"""
###Load

#CONSUMER IS AN OBJECT WHICH REPRESENTS APPLICATION
#Create a consumer, which uses TW_CONSUMER_KEY and TW_CONSUMER_SECRET to identify our app uniquely
# consumer = oauth2.Consumer(constants.TW_CONSUMER_KEY, constants.TW_CONSUMER_SECRET)     #"""Getting OAuth access token SEC 113"""
# """This is just used to identify the app, cannot be used to make requests"""     #"""Getting OAuth access token SEC 113"""
# client = oauth2.Client(consumer)     #"""Getting OAuth access token SEC 113"""
#
# #Use the client to perform a request for the request token
# response, content = client.request(constants.TW_REQUEST_TOKEN_URL, 'POST')     #"""Getting OAuth access token SEC 113"""
# if response.status!=200:     #"""Getting OAuth access token SEC 113"""
#     print("An error occurred getting the request token from Twitter.")     #"""Getting OAuth access token SEC 113"""
#
# #Get the request token parsing the query string returned
# request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))         #"""Getting OAuth access token SEC 113"""
request_token = get_request_token()

"""Lecture 111 talked about debugging"""

#www.ourwebsite.com "login with twitter button"
#they press Sign In or Authorize
#Twitter sends them back to e.g. www.ourwebsite.com/auth****
# """With no website to return to, twitter will generate a pin code"
#we get teh auth code + request token -> twotter -> access token

# #Ask the user to authorize our app and give us the pini code
print("Goto the following site in your browser:")     #"""Getting OAuth access token SEC 113"""
print("{}?oauth_token={}".format(constants.TW_AUTHORIZATION_URL, request_token['oauth_token']))     #"""Getting OAuth access token SEC 113"""


oauth_verifier = input("What is the PIN? ")     #"""Getting OAuth access token SEC 113"""

#Put a request token into an object "token" Used to combine oauth_token and the oauth_token_secret and verifier
#Create a Token object which contains the request token, and the verifier
token = oauth2.Token(request_token['oauth_token'],request_token['oauth_token_secret'] )     #"""Getting OAuth access token SEC 113"""

#Add oauth_verifier to the token
token.set_verifier(oauth_verifier)     #"""Getting OAuth access token SEC 113"""

#recreate client object with the token identifier
#Create a client with our consumer (our app) and the newly created (and verified) token
client = oauth2.Client(consumer, token)     #"""Getting OAuth access token SEC 113"""

#Ask Twitter fore an access token, and Twitter knows it shoudl give us it because we've verified the request token

response, content = client.request(constants.TW_ACCESS_TOKEN_URL, 'POST')     #"""Getting OAuth access token SEC 113"""
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))     #"""Getting OAuth access token SEC 113"""
print(access_token['screen_name'])     #"""Getting OAuth access token SEC 113"""

#Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])          #"""Performing Twitter Requests : Getting Images Sec 114"""
authorized_client = oauth2.Client(consumer, authorized_token)          #"""Performing Twitter Requests : Getting Images Sec 114"""

#Create User  def __init__(self,email, first_namu
#  e,last_name, oauth_token, oauth_token_secret, id=None):

"""Could I get this from the twitter request in the user file?"""

response, content = authorized_client.request('https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true','GET')
if response.status != 200:                           #"""Performing Twitter Requests : Getting Images Sec 114"""
    print("An error occurred when searching!")       #"""Performing Twitter Requests : Getting Images Sec 114"""
infos = json.loads(content.decode('utf-8'))          #"""Performing Twitter Requests : Getting Images Sec 114"""


email=infos['email']
screen_name=infos['screen_name']                     #"""Performing Twitter Requests : Getting Images Sec 114"""
name=infos['name'].split(" ")
if len(name)== 3:
    first_name=name[0]
    middle_name=name[1]
    last_name=name[2]
elif len(name)== 2:
    first_name=name[0]
    last_name=name[1]
    middle_name=''
elif len(name)== 1:
    first_name = name[0]
    middle_name = ''
    last_name = ''

response, content = authorized_client.request('https://api.twitter.com/1.1/account/update_profile.json?name={}'.format(access_token['screen_name']),'POST')


user=User(email=email, screen_name=screen_name, first_name=first_name, middle_name=middle_name,last_name=last_name, oauth_token=access_token['oauth_token'],oauth_token_secret=access_token['oauth_token_secret'])
#print(user)
user.save_to_db()


#Make Twitter API calls! #Returning a list of tweets
# response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computer+filter:images','GET')          #"""Performing Twitter Requests : Getting Images Sec 114"""
# if response.status != 200:                              #"""Performing Twitter Requests : Getting Images Sec 114"""
#     print("An error occurred when searching!")          #"""Performing Twitter Requests : Getting Images Sec 114"""
# tweets = json.loads(content.decode('utf-8'))            #"""Performing Twitter Requests : Getting Images Sec 114"""

#for tweet in tweets['statuses']:          #"""Performing Twitter Requests : Getting Images Sec 114"""
#    print(tweet['text'])          #"""Performing Twitter Requests : Getting Images Sec 114"""

