from flask import (
    current_app,
    request,
    session,
)
from flask_restful import Resource
from requests_oauthlib import OAuth1Session

from ..extensions import restful_api


@restful_api.resource('/login')
class Login(Resource):
    def get(self):
        app_hash = request.args['hash']
        oauth1_session = OAuth1Session(
            current_app.config['USOS_CONSUMER_KEY'],
            current_app.config['USOS_CONSUMER_SECRET'],
            callback_uri=restful_api.url_for(
                OAuthAuthorized,
                app_hash=app_hash,
                _external=True,
            ),
        )
        response = oauth1_session.fetch_request_token(
            current_app.config['USOS_REQUEST_TOKEN_URL'],
            params=current_app.config['USOS_SCOPES'],
        )
        if response:
            session['oauth_token'] = response['oauth_token']
            session['oauth_token_secret'] = response['oauth_token_secret']
            authorize_url = oauth1_session.authorization_url(
                current_app.config['USOS_AUTHORIZE_URL'],
            )
            return {'url': authorize_url}
        else:
            return {'message': 'Unauthorized'}, 401


@restful_api.resource('/oauth-authorized/<app_hash>')
class OAuthAuthorized(Resource):
    def get(self, app_hash):
        oauth_token = request.args.get('oauth_token', '')
        oauth_verifier = request.args.get('oauth_verifier', '')
        oauth_token_secret = session['oauth_token_secret']

        oauth1_session = OAuth1Session(
            current_app.config['USOS_CONSUMER_KEY'],
            current_app.config['USOS_CONSUMER_SECRET'],
            resource_owner_key=oauth_token,
            resource_owner_secret=oauth_token_secret,
            verifier=oauth_verifier
        )
        resp = oauth1_session.fetch_access_token(
            current_app.config['USOS_ACCESS_TOKEN_URL'],
        )
        session['oauth_token'] = resp['oauth_token']
        session['oauth_token_secret'] = resp['oauth_token_secret']
