import bleach
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.tags import bp
from app.models import Tag
from .forms import TagForm


@bp.route('/', methods=["GET", "POST"])
@bp.route('/<int:id>', methods=["GET", "POST"])
@login_required
def index(id=None):
    if not current_user.is_admin:
        abort(403) 
    form = TagForm()
    tag = None
    if id:
        tag = Tag.query.get_or_404(id)

    if form.validate_on_submit():
        if id:
            tag.name = form.name.data
        else:
            tag = Tag(name=bleach.clean(form.name.data))
            if not Tag.query.filter_by(name=tag.name).first():  # not Already exist
                db.session.add(tag)
            
        db.session.commit()
        tag = None
    
    tags = Tag.query.all()
    return render_template('tags/index.html', form=form, tags=tags, current_tag=tag)


@bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    if not current_user.is_admin:
        abort(403) 
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags.index'))
