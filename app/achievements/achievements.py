from datetime import datetime
import imghdr
import os
import re
import bleach

from flask import Response, abort, current_app, jsonify, make_response, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from werkzeug.utils import secure_filename

from app import db
from app.models import Tag
from app.achievements import bp

from app.models import Article
from app.models import ImagesArticle
from .forms import ArticleForm


@bp.route('/')
def index():
    articles = Article.query.all()
    return render_template('achievements/index.html', achievements=articles)

@bp.route('/<int:id>')
def view(id):
    article = Article.query.get_or_404(id)
    images = ImagesArticle.query.filter_by(article_id = id).all()
    print(images)
    return render_template('achievements/view.html', achievement=article, gallery=images)



@bp.route('/edit/')
@login_required
def list():
    if not current_user.is_admin:
        abort(403) 
    articles = Article.query.all()
    return render_template('achievements/list.html', achievements=articles)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        abort(403) 
    errors = []
    form = ArticleForm()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]

    article = Article.query.get_or_404(id)

    # POST
    if form.validate_on_submit():
        error = fill_article(article, form)
        if not error:
            # DB
            db.session.commit()
            fill_gallery(article, form)
            return redirect(url_for('achievements.list'))

        errors.append(error)

    form.title.default = article.title
    form.subtitle.default = article.subtitle
    form.content.default = article.content
    form.tags.default = [t.id for t in article.tags]
    form.process()
    return render_template('achievements/edit.html', achievement=article, form=form, errors=errors)


@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403) 
    errors = []
    form = ArticleForm()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]

    # POST
    if form.validate_on_submit():
        article = Article()
        error = fill_article(article, form)
        if not error:
            # DB
            db.session.add(article)
            db.session.commit()
            fill_gallery(article, form)
            return redirect(url_for('achievements.list'))

        errors.append(error)

    return render_template('achievements/edit.html', form=form, errors=errors)

@bp.route("/delete/<int:id>", methods=['GET'])
@login_required
def delete(id):
    if not current_user.is_admin:
        abort(403) 
    article = Article.query.get_or_404(id)

    #Cover image
    path = f"{current_app.root_path}/static/{article.cover_img}"
    if os.path.exists(path):
        os.remove(path)

    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('achievements.list'))


@bp.route('/upload/', methods=['POST'])
@login_required
def image_upload():
    if not current_user.is_admin:
        abort(403) 
    file = request.files.get('file')
    if file:
        filename = check_image(file)
        if not filename:
            output = make_response(404)
            output.headers['Error'] = 'Incorrect image file'
            return output 
        ts = round(datetime.timestamp(datetime.now()))
        uri = f"/files/{ts}-{filename}"
        file.save(f"{current_app.root_path}/static/{uri}")
        return jsonify({'location' : f'/static/{uri}'})
    output = Response(status=400)
    output.headers['Error'] = 'Image failed to upload'
    return output 



def check_image(file):
        """
        Return a secure filename if image is correct. Otherwise return False.
        """
        # Check extension
        match = re.findall('^$|([^\s]+(\.(jpe?g|png|gif|bmp))$)', file.filename)
        if not match: 
            return False

        # Check file header
        stream = file.stream
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)  # imghdr auto-detect format based on header
        if not format:
            return False
        
        return secure_filename(file.filename)


def fill_article(article, form):
    """
    Fill the Article class with the form object. 
    Return None  if success.
    Return <error_msg> if error.
    """
    # Text fields
    article.title = bleach.clean(form.title.data)
    article.subtitle = bleach.clean(form.subtitle.data)
    if not form.content.data:
        return "Content is required"
    article.content = form.content.data
    article.tags = [Tag.query.get(id) for id in form.tags.data]

    # Cover image
    img = request.files['cover_img']
    if img.filename:
        filename = check_image(img)
        if not filename:
            return "Image file is invalid"
        ts = round(datetime.timestamp(datetime.now()))
        uri = f"/files/{ts}-{filename}"
        img.save(f"{current_app.root_path}/static/{uri}")
        article.cover_img = uri

    return None

def fill_gallery(article, form):
    """
    Create and fill ImagesArticle row that act as an images gallery for each Article
    """
    imgs = form.images.data
    print(imgs)
    for img in imgs:
        if img.filename:
            imagearticle = ImagesArticle()
            filename = check_image(img)
            if not filename:
                return "Image file is invalid"
            ts = round(datetime.timestamp(datetime.now()))
            uri = f"/files/{ts}-{filename}"
            img.save(f"{current_app.root_path}/static/{uri}")
            imagearticle.image = uri
            imagearticle.article_id = article.id
            db.session.add(imagearticle)
    db.session.commit()
    return None
