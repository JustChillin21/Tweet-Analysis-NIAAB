import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.TW_CONSUMER_KEY, constants.TW_CONSUMER_SECRET)

def get_request_token():
    """This is just used to identify the app, cannot be used to make requests"""  # """Getting OAuth access token SEC 113"""
    client = oauth2.Client(consumer)  # """Getting OAuth access token SEC 113"""

    # Use the client to perform a request for the request token
    response, content = client.request(constants.TW_REQUEST_TOKEN_URL,'POST')  # """Getting OAuth access token SEC 113"""
    if response.status != 200:  # """Getting OAuth access token SEC 113"""
        print(
            "An error occurred getting the request token from Twitter.")  # """Getting OAuth access token SEC 113"""

    # Get the request token parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))  # """Getting OAuth access token SEC 113"""

def get_oauth_verifier(request_token):
    # Ask the user to authorize our app and give us the pini code
    print("Goto the following site in your browser:")  # """Getting OAuth access token SEC 113"""
    print(get_oauth_verifier_url(request_token))  # """Getting OAuth access token SEC 113"""

    return input("What is the PIN? ")  # """Getting OAuth access token SEC 113"""

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.TW_AUTHORIZATION_URL,request_token['oauth_token'])

def get_access_token(request_token, oauth_verifier):
    # Put a request token into an object "token" Used to combine oauth_token and the oauth_token_secret and verifier
    # Create a Token object which contains the request token, and the verifier
    token = oauth2.Token(request_token['oauth_token'],
                         request_token['oauth_token_secret'])  # """Getting OAuth access token SEC 113"""


    # Add oauth_verifier to the token
    token.set_verifier(oauth_verifier)  # """Getting OAuth access token SEC 113"""

    # recreate client object with the token identifier
    # Create a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)  # """Getting OAuth access token SEC 113"""

    # Ask Twitter fore an access token, and Twitter knows it shoudl give us it because we've verified the request token

    response, content = client.request(constants.TW_ACCESS_TOKEN_URL,
                                       'POST')  # """Getting OAuth access token SEC 113"""
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))  # """Getting OAuth access token SEC 113"""
    print(access_token['screen_name'])  # """Getting OAuth access token SEC 113"""
    return access_token

def get_names(name):
    first_name, middle_name, last_name = ('','','')
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
    return first_name, middle_name, last_name
