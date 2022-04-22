from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.models import User
from app.user import bp

from app.models import Article, Tag
from app.user.forms import LoginForm, ArticleForm


@bp.route('/')
@bp.route('/index/')
def index():
    return render_template('user/index.html')


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit():  # POST processing
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            errors.append("Pas d'utilisateurs avec cet email")
        elif not user.check_password(form.password.data):
            errors.append("Mot de passe incorrect")
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':  # Check if there is a next_page and if the next_page is a relative path
                next_page = url_for('user.index')
            return redirect(next_page)
    return render_template('user/login.html', form=form, errors=errors)


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/achievements/')
@login_required
def achievements():
    articles = Article.query.all()
    return render_template('user/achievements.html', achievements=articles)


@bp.route('/achievements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def achievements_edit(id):
    form = ArticleForm()
    form.tags.choices = Tag.query.all()
    article = Article.query.get_or_404(id)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        article.title = form.title.data
        article.subtitle = form.title.data
        article.content = form.content.data
        print(f'---------------------{form.choices.data}')
        return redirect(url_for('user.achievements'))

    form.title.default = article.title
    form.subtitle.default = article.subtitle
    form.content.default = article.content
    form.tags.default = article.tags
    form.process()
    return render_template('user/achievements_edit.html', achievement=article, form=form)


@bp.route('/achievements/new/')
@login_required
def achievements_new():
    form = ArticleForm()
    return render_template('user/achievements_edit.html', form=form)
