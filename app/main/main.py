from flask import redirect, render_template, request, url_for

from app import db
from app.main import bp
from app.models import Action, Article, User
from app.user.forms import SignupForm

@bp.route('/')
def index():
    articles = Article.query.limit(10).all()
    return render_template("index.html", achievements=articles)

@bp.route('/contact/')
def contact():
    return render_template("contact.html")

@bp.route('/legals/')
def legals():
    return render_template("legals.html")

@bp.before_app_first_request
def firstrequest():
    print('First Request -- Creating and initializing DB')
    db.create_all()
    Action.create_table()

@bp.before_app_request
def firstconnection():
    if len(User.query.all()) == 0:  # No user in db
        form = SignupForm()
        errors = []

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            u = User(username=username, email=email, is_admin=True)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('user.login'))
        
        if request.method == 'POST' and not form.validate():
            errors.append(form.errors)

        return render_template('user/firstconnection.html', form=form, errors=errors)