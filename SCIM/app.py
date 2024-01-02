from flask import Flask, request, redirect, session, url_for
from flask_session import Session
import requests
import urllib
import urllib.parse
from requests.auth import HTTPBasicAuth
app = Flask(__name__)

# Configure the session extension
# You can choose a different storage type
app.config['SESSION_TYPE'] = 'filesystem'
# Replace with a strong secret key
app.config['SECRET_KEY'] = 'your_secret_key'
Session(app)


# External identity system configuration
AUTHORIZATION_SERVER = 'https://migtenantqa1-hs-sso-stg.iams.hs.ocs.oraclecloud.com/ms_oauth/oauth2/endpoints/migtenantqa1_oracle/authorize'
TOKEN_ENDPOINT = 'https://migtenantqa1-hs-sso-stg.iams.hs.ocs.oraclecloud.com/ms_oauth/oauth2/endpoints/migtenantqa1_oracle/tokens'
CLIENT_ID = 'migtenantqa1.eclinical-portal-ac_CNE1'
CLIENT_SECRET = 'abcdefghijklmnopqrstuvwxyz0123456789'




# Adjust as needed
REDIRECT_URI = 'http://migtenantqa1.clinicalone.oraclecloud.com:5000/callback.html'
cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

REDIRECT_URI1 = "https://migtenantqa1-hs-sso-stg.iams.hs.ocs.oraclecloud.com/ms_oauth/oauth2/endpoints/migtenantqa1_oracle/tokens?"


@app.route('/')
def login():
    # Construct the authorization URL
    authorization_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        # Replace with desired scopes
        'scope': 'migtenantqa1.eclinical-portal.svc migtenantqa1.iams_userprofile.read',
    }
    authorization_url = AUTHORIZATION_SERVER + '?' + \
        urllib.parse.urlencode(authorization_params)

    return redirect(authorization_url)


@app.route('/callback.html')
def callback():
    # Additional headers you want to include in the request
    code = request.args.get('code')
    # Exchange the code for tokens, including the custom headers
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
# Make the initial GET request to the authorization endpoint with Basic Authentication
    response = requests.post(
        TOKEN_ENDPOINT, params=token_data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    tokens = response.json()
    print(tokens)

    # Store the access token in the session
    session['access_token'] = tokens['access_token']
    if response.status_code == 200:
        auth_token_data = response.json()
        access_token = auth_token_data.get('access_token')
        refresh_token = auth_token_data.get('refresh_token')
        print('Access Token:', access_token)
        print('Refresh Token:', refresh_token)
    else:
        print('Token exchange failed.')

    # Redirect to a page that indicates the user is authenticated
    return redirect(url_for('authenticated'))


@app.route('/authenticated')
def authenticated():
    # Check if the user is authenticated based on the presence of the access token in the session
    if 'access_token' in session:
        return 'You are authenticated!'
    else:
        return 'You are not authenticated.'
# Function to refresh the access token using the refresh token


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return 'You are logged out!'


if __name__ == '__main__':
    app.run(debug=True)
