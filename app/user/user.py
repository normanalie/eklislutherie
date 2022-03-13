from flask import render_template

from app import db
from app.user import bp

from app.user.forms import LoginForm


@bp.route('/login/')
def login():
    form = LoginForm()
    return render_template("user/login.html", form=form)