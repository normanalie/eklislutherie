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

SECRET_KEY = os.environ.get('SECRET_KEY') or 'yTnSN65a'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
