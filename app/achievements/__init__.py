from flask import Blueprint

bp = Blueprint('achievements', __name__, url_prefix="/achievements")

from app.achievements import achievements