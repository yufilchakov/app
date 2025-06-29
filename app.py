from flask import Flask
from flask_migrate import Migrate
from models import db
from routes.auth import auth


def create_app():
    """Фабрика для создания и настройки экземпляра Flask приложения."""
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(auth)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
