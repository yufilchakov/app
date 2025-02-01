import os
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_value_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {}


class User(UserMixin):
    def __init__(self, oid, profile):
        self.oid = oid
        self.profile = profile


@login_manager.user_loader
def load_user(oid):
    return users.get(oid)


@app.route('/')
def index():
    return render_template('index.html', user=current_user)


@app.route('/auth')
def auth():
    return redirect(get_authorization_url())


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_access_token(code)
    profile = get_user_details(token)
    
    if profile:
        user = User(profile['oid'], profile)
        users[profile['oid']] = user
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash('Error retrieving user details')
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def get_authorization_url():
    return f"{os.environ['OAUTH_AUTHORITY']}{os.environ['OAUTH_AUTHORIZE_ENDPOINT']}?client_id={os.environ['OAUTH_APP_ID']}&response_type=code&redirect_uri={os.environ['OAUTH_REDIRECT_URI']}&scope={os.environ['OAUTH_SCOPES']}"


def get_access_token(code):
    token_url = f"{os.environ['OAUTH_AUTHORITY']}{os.environ['OAUTH_TOKEN_ENDPOINT']}"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ['OAUTH_REDIRECT_URI'],
        'client_id': os.environ['OAUTH_APP_ID'],
        'client_secret': os.environ['OAUTH_APP_PASSWORD']
    }
    response = requests.post(token_url, data=data)
    return response.json().get('access_token')


def get_user_details(access_token):
    
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()


if __name__ == '__main__':
    app.run(port=3000)
