import oauth2
import json
from user import User
from twitter_utils import consumer, get_request_token, get_oauth_verifier, get_access_token, get_names

def create_user(email):


###GET REQUEST TOKEN
    # """This is just used to identify the app, cannot be used to make requests"""
    request_token = get_request_token()
###END OF GET REQUEST TOKEN

# ##GET OAUTH VERIFIER
    oauth_verifier = get_oauth_verifier(request_token)
##END OF GET OAUTH 2 VERIFIER

##RECREATE CLIENT WITH VERIFIER

#
#     #recreate client object with the token identifier
#     #Create a client with our consumer (our app) and the newly created (and verified) token
#     client = oauth2.Client(consumer, token)
#
# #Ask Twitter fore an access token, and Twitter knows it should give us it because we've verified the request token
    access_token = get_access_token(request_token, oauth_verifier)
#     print(access_token['screen_name'])
##END OF RECREATE CLIENT WITH VERIFIER

    #Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user

    authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
    authorized_client = oauth2.Client(consumer, authorized_token)

##GET ACCOUNT CREDENTIALS AND BUILD USER
#"""Performing Twitter Requests : Getting Images Sec 114"""

    response, content = authorized_client.request('https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true','GET')
    if response.status != 200:
        print("An error occurred when searching!")

    infos = json.loads(content.decode('utf-8'))
    email=infos['email']
    screen_name=infos['screen_name']
    name=infos['name'].split(" ")
    first_name, middle_name, last_name=get_names(name)
    #
    # if len(name)== 3:
    #     first_name=name[0]
    #     middle_name=name[1]
    #     last_name=name[2]
    # elif len(name)== 2:
    #     first_name=name[0]
    #     last_name=name[1]
    #     middle_name=''
    # elif len(name)== 1:
    #     first_name = name[0]
    #     middle_name = ''
    #     last_name = ''

    user=User(email=email, screen_name=screen_name, first_name=first_name, middle_name=middle_name,last_name=last_name, oauth_token=access_token['oauth_token'],oauth_token_secret=access_token['oauth_token_secret'])
    return user