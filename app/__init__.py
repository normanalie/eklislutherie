from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from app import models
from . import main


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main.bp)

    return app