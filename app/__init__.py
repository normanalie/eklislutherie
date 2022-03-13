from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

from app import models
from . import main, user


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    login.init_app(app)

    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)

    return app