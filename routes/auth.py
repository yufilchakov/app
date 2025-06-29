from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from models import User, db
import requests
import os

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    """Отображает главную страницу с текущим годом и информацией о пользователе."""
    current_year = datetime.now().year
    return render_template('index.html', user=current_user, year=current_year)


@auth.route('/auth')
def auth_route():
    """Перенаправляет пользователя на страницу авторизации."""
    return redirect(get_authorization_url())


@auth.route('/callback')
def callback():
    """Обрабатывает обратный вызов после авторизации, получает токен доступа и данные пользователя."""
    code = request.args.get('code')
    token = get_access_token(code)
    profile = get_user_details(token)

    if profile:
        user = User.query.get(profile['oid'])
        if not user:
            user = User(
                id=profile['oid'],
                email=profile.get('mail'),
                name=profile.get('displayName'),
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('auth.index'))
    else:
        flash('Ошибка получения данных пользователя')
        return redirect(url_for('auth.index'))


@auth.route('/logout')
@login_required
def logout():
    """Выходит из системы и перенаправляет на главную страницу."""
    logout_user()
    return redirect(url_for('auth.index'))


def get_authorization_url():
    """Формирует и возвращает URL для авторизации пользователя."""
    return (f'{os.environ['OAUTH_AUTHORITY']}{os.environ['OAUTH_AUTHORIZE_ENDPOINT']}?'
            f'client_id={os.environ['OAUTH_APP_ID']}&response_type=code&redirect_uri={os.environ['OAUTH_REDIRECT_URI']}'
            f'&scope={os.environ['OAUTH_SCOPES']}')


def get_access_token(code):
    """Получает токен доступа по коду авторизации."""
    token_url = f'{os.environ['OAUTH_AUTHORITY']}{os.environ['OAUTH_TOKEN_ENDPOINT']}'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ['OAUTH_REDIRECT_URI'],
        'client_id': os.environ['OAUTH_APP_ID'],
        'client_secret': os.environ['OAUTH_APP_PASSWORD'],
    }
    response = requests.post(token_url, data=data)
    return response.json().get('access_token')


def get_user_details(access_token):
    """Получает данные пользователя по токену доступа."""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()
