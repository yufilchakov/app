import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from dotenv import load_dotenv
from config import Config

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


def check_env_variables():
    """Проверяет наличие обязательных переменных окружения."""
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'OAUTH_APP_ID',
        'OAUTH_APP_PASSWORD',
        'OAUTH_AUTHORITY',
        'OAUTH_AUTHORIZE_ENDPOINT',
        'OAUTH_TOKEN_ENDPOINT',
        'OAUTH_REDIRECT_URI',
        'OAUTH_SCOPES',
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f'Variable {var} is not set in the environment.')


def create_app():
    """Создает и настраивает экземпляр Flask приложения."""
    app = Flask(__name__)
    check_env_variables()
    app.config.from_object(Config)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from routes.auth import auth as auth_blueprint

        app.register_blueprint(auth_blueprint)

        db.create_all()

    return app
