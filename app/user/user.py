from flask import  redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required


from werkzeug.urls import url_parse

from app import db
from app.models import User
from app.user import bp

from app.models import Tag
from app.user.forms import LoginForm, SignupForm


@bp.route('/')
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


@bp.route('/manage/')
@login_required
def manage():
    users = User.query.all()
    return render_template('user/manage.html', users=users)


@bp.route('/manage/<int:id>')
@login_required
def edit(id):
    pass


@bp.route('/manage/new/')
@login_required
def new():
    form = SignupForm()
    return render_template('user/edit.html', form=form)


@bp.route('/account/')
@login_required
def account():
    pass


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('user.manage'))


