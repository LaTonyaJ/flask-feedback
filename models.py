from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user with hashed password"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        user = cls(username=username, password=hashed_utf8,
                   first_name=first_name, last_name=last_name, email=email)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Is your password right?"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    feedback = db.relationship(
        'Feedback', cascade='all, delete-orphan', backref='user')


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String(20), db.ForeignKey(
        'users.username'), nullable=False)
