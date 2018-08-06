from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    todos = db.relationship('Todo', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        gerate md5 hash the email is converted lower case as required by
        gravatar service.
        md5 support in python works on bytes not strings so string is encoded
        as bytes before being passed to the hashing function.
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return f'<User {self.username}>'


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    actionable = db.Column(db.String(140))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Todo {self.name}, {self.start}, {self.end}, {self.actionable}>'


@login.user_loader
def user_loader(id):
    """Given *user_id*, return the associated User object.

    :param unicode user id: id user to retrieve

    """
    return User.query.get(int(id))

