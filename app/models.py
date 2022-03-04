from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


    def __repr__(self):
        return f'<User: {self.username}>'


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'<Action: {self.name}>'


class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
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
    date = db.Column(db.DateTime, nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    article = db.relationship('Article')
    action = db.relationship('Action')
    user = db.relationship('User')

    def __repr__(self):
        return f'<ArticleHistory: {self.action}: {self.article} by {self.user}>'