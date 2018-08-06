import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir, 'todo.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
