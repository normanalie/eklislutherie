from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'user.login'

from app import models
from . import main, user, achievements, tags


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    login.init_app(app)

    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(achievements.bp)
    app.register_blueprint(tags.bp)

    return app