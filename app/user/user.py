from flask import render_template

from app import db
from app.user import bp


@bp.route('/login/')
def login():
    return render_template("user/login.html")