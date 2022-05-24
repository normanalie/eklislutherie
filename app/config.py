"""Flask configuration."""
"""
To start app: 
    set FLASK_APP=app
    set FLASK_DEBUG=True
    set FLASK_ENV=development
    python eklislutherie.py
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SERVER_NAME=os.environ.get('SERVER_NAME')
APPLICATION_ROOT=os.environ.get('APPLICATION_ROOT') or '/'
PREFERRED_URL_SCHEME="https"

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
