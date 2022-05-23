from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app import achievements
from app.models import User
from app.achievements import bp

from app.models import Article


@bp.route('/')
def index():
    articles = Article.query.all()
    return render_template('achievements/index.html', achievements=articles)

@bp.route('/<int:id>')
def view(id):
    article = Article.query.get_or_404(id)
    return render_template('achievements/view.html', achievement=article)