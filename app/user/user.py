from distutils.log import error
import re
import bleach
from flask import  redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError


from werkzeug.urls import url_parse

from app import db
from app.models import User
from app.user import bp

from app.models import Tag
from app.user.forms import EditForm, LoginForm, SignupForm


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


@bp.route('/manage/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = EditForm()
    errors = []

    u = User.query.get_or_404(id)

    if request.method == 'POST':
        if form.password.data != form.password_confirmation.data:
            errors.append('Les mots de passes ne correspondent pas')
    if form.validate_on_submit():
        err = fill_user(u, form, new=False)
        if not err:
            db.session.commit()
            return redirect(url_for('user.manage'))
        errors.append(err)

    form.username.default = u.username
    form.email.default = u.email
    form.is_admin.default = u.is_admin
    form.is_active.default = u.is_active
    form.process()

    return render_template('user/edit.html', form=form, errors=errors)



@bp.route('/manage/new/', methods=['GET', 'POST'])
@login_required
def new():
    form = SignupForm()
    errors = []

    if request.method == 'POST':
        if form.password.data != form.password_confirmation.data:
            errors.append('Les mots de passes ne correspondent pas')
    if form.validate_on_submit():
        u = User()
        err = fill_user(u, form, new=True)
        if not err:
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('user.manage'))
        errors.append(err)

    return render_template('user/edit.html', form=form, errors=errors)


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


def check_email_format(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def check_email_db(email):
    u = User.query.filter_by(email=email).first()
    return False if u else True


def fill_user(user, form, new=True):
    """
    Fill the  given User based on form datas.
    Return None if succes
    Return <error_message> else.
    """
    user.username = bleach.clean(form.username.data)
    email = bleach.clean(form.email.data)
    if not check_email_format(email):
        return 'Email invalide'
    elif user.email != email and not check_email_db(email):
        return 'Email déjà utilisé'

    user.email = email
    if current_user.id == user.id and form.is_admin.data != user.is_admin:  # Admin can't remove his own rights
        return 'Vous ne pouvez pas changer vos droits administrateur'
    user.is_admin = form.is_admin.data

    if current_user.id == user.id and form.is_active != user.is_active: 
        return "Vous ne pouvez pas changer votre status"
    user.is_active = form.is_active.data

    if form.password.data:
        if len(form.password.data)<8:
            return "Le mot de passe doit faire au moins 8 caractères"
        user.set_password(form.password.data)

    return None
