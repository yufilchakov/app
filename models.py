from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Модель пользователя для работы с базой данных."""
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.name}>'
