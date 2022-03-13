from flask import render_template

from app import db
from app.main import bp
from app.models import Article

@bp.route('/')
@bp.route('/index/')
def index():
    articles = Article.query.limit(10).all()
    return render_template("index.html", achievements=articles)

@bp.route('/contact/')
def contact():
    return render_template("contact.html")

@bp.route('/legals/')
def legals():
    return render_template("legals.html")