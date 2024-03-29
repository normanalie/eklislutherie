from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask_login import UserMixin

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def create_table():
        if Action.query.first() == None:
            actions=['login', 'logout', 'create', 'delete', 'update', 'publish', 'unpublish']
            for action in actions:
                a = Action(name=action)
                db.session.add(a)
            db.session.commit()

    def __repr__(self):
        return f'<Action: {self.name}>'


class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    action_id = db.Column(db.Integer(), db.ForeignKey('action.id'), nullable=False)
    by_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', foreign_keys=[user_id])
    action = db.relationship('Action')
    by_user = db.relationship('User', foreign_keys=[by_user_id])

    def __repr__(self):
        return f'<UserHistory: {self.action}: {self.user} by {self.by_user}>'


tags = db.Table('tags', 
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    subtitle = db.Column(db.String(128))
    content = db.Column(db.Text, nullable=False)
    cover_img = db.Column(db.String(128), nullable=False)
    
    tags = db.relationship('Tag', secondary='tags', backref=db.backref('articles', lazy=True))
    images = db.relationship('ImagesArticle')

    def __repr__(self):
        return f'<Article: {self.title}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'<Tag: {self.name}>'


class ArticleHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    article = db.relationship('Article')
    action = db.relationship('Action')
    user = db.relationship('User')

    def __repr__(self):
        return f'<ArticleHistory: {self.action}: {self.article} by {self.user}>'
    
class ImagesArticle(db.Model):
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)
    image = db.Column(db.String(128), primary_key=True)

    article = db.relationship('Article')

    def __repr__(self):
        return f'<ImagesArticle: {self.image}: {self.article_id}>'