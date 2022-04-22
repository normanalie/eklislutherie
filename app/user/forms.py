from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    cover_img = FileField("Cover Image", validators=[regexp(u'[^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$')])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    tags = SelectMultipleField("Tags")
    submit = SubmitField('Save')