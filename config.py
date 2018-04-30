from os import environ, path
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENV = environ.get('FLASK_ENV', 'development')
    APP = environ.get('FLASK_APP', 'app.py')
    HOST = environ.get('HOST', '0.0.0.0')
    PORT = environ.get('PORT', 5000)
    APP_NAME = environ.get('APP_NAME', 'testar')
    THREADED = environ.get('THREADED', True)
    DEBUG = environ.get('DEBUG', True)
    SECRET_KEY = environ.get('SECRET_KEY', 'SOME_SECRET')
    TOKEN_EXP = environ.get('TOKEN_EXP', 3600 * 24 * 24)

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
