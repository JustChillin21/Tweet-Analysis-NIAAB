"""FLASK"""

from flask import Flask, render_template,session,redirect
from twitter_utils import get_request_token, get_oauth_verifier_url

app = Flask(__name__)
app.secret_key='d5jQGvNZzoLSmg6eut' #Signing session using secret key #Section 10 Lession 120

@app.route('/') ## http://127.0.0.1:4995/  #Section 10 Lession 120
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    # request_token=get_request_token()                 #Cleaned it up by rolling into one line #Section 10 Lession 120
    session['request_token'] = get_request_token()

    #Section 10 Lession 120 #redirect the user to Twitter so they can confirm authorization
    return redirect(get_oauth_verifier_url(session['request_token']))

app.run(port=4995)

