"""FLASK"""

from flask import Flask, render_template, session, redirect, request, url_for, g
from menu import Menu
from save import create_user
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User

app = Flask(__name__)
app.secret_key='d5jQGvNZzoLSmg6eut' #Signing session using secret key #Section 10 Lession 120

Menu.display_table_columns() #initialize database and return column names

@app.before_request #Section 10-123
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_token((session['screen_name'],'screen_name'))


@app.route('/') ## http://127.0.0.1:4995/  #Section 10 Lession 120
def homepage():
    if 'screen_name' in session:
        user=g.user.first_name
    else:
        user="There"
    return render_template('home.html',user=user)
    #
    # return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    # request_token=get_request_token()                 #Cleaned it up by rolling into one line #Section 10 Lession 120
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    session['request_token'] = get_request_token()
    return redirect(get_oauth_verifier_url(session['request_token']))
    #Section 10 Lession 120 #redirect the user to Twitter so they can confirm authorization


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)
    screen_name=access_token['screen_name']
    token=Menu.param_type(access_token['screen_name'])
    print("loading from user...{}{}".format(screen_name, token))

    user=User.load_from_db_by_token(token)
    if not user:
        user=create_user(access_token)
        user.save_to_db()
    session['screen_name']=user.screen_name
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'screen_name' in session:
        return render_template('profile.html', user=g.user)
    return redirect(url_for('twitter_login'))

@app.route('/search')
def search():
    topic=request.args.get('q')
    filterby=request.args.get('fb')
    tweets = g.user.tw_request(topic=topic, filterby=filterby)
    tweet_texts=[tweet['text'] for tweet in tweets['statuses']]
    return render_template('search.html', content=tweet_texts)

app.run(port=4995, debug=True)

