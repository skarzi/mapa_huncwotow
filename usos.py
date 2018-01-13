import configparser

from flask import Flask, redirect, request, session
from flask_cors import CORS
from flask_session import Session
from requests_oauthlib import OAuth1Session

app = Flask(__name__)
app.secret_key = 'suapdajhfjashdaj'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)
Session(app)


parser = configparser.ConfigParser()
parser.read('./conf.ini')

base_url = 'apps.usos.pw.edu.pl/'
usosapi_base_url_secure = 'https://' + base_url
usosapi_base_url = 'http://' + base_url

request_token_url = usosapi_base_url_secure + 'services/oauth/request_token'
authorize_url = usosapi_base_url + 'services/oauth/authorize'
access_token_url = usosapi_base_url_secure + 'services/oauth/access_token'
tt_url = 'https://apps.usos.pw.edu.pl/services/tt/user'


@app.route("/auth/<username>")
def auth(username):
    oauth_token = request.args.get('oauth_token', '')
    oauth_verifier = request.args.get('oauth_verifier', '')

    oauth_token2 = session['oauth_token']
    oauth_token_secret = session['oauth_token_secret']

    auth = OAuth1Session(
        parser['USOS']['consumerKey'],
        parser['USOS']['consumerSecret'],
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        verifier=oauth_verifier
    )
    resp = auth.fetch_access_token(access_token_url)
    session['oauth_token'] = resp['oauth_token']
    session['oauth_token_secret'] = resp['oauth_token_secret']
    resp = auth.get(tt_url)
    return resp.content


def _read_token(content):
    return content['oauth_token'], content['oauth_token_secret']


parser = configparser.ConfigParser()
parser.read('./conf.ini')


@app.route('/authorize/<username>')
def authorize(username):
    auth = OAuth1Session(
        parser['USOS']['consumerKey'],
        parser['USOS']['consumerSecret'],
        callback_uri='http://localhost:5000/auth/{}'.format(username))
    resp = auth.fetch_request_token(request_token_url, params={'scopes': 'studies'})
    session['oauth_token'] = resp['oauth_token']
    session['oauth_token_secret'] = resp['oauth_token_secret']
    if resp:
        auth_url = auth.authorization_url(authorize_url)
        return redirect(auth_url)
    else:
        return 'Error', 404
