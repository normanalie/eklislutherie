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


SERVER_NAME=os.getenv('SERVER_NAME')
APPLICATION_ROOT=os.getenv('APPLICATION_ROOT') or '/'
PREFERRED_URL_SCHEME="https"

SECRET_KEY = os.getenv('SECRET_KEY') or 'fakeSecretKeyToChangeInProduction'

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 60,
    'pool_pre_ping': True
}
