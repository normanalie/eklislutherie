from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')


class SignupForm(FlaskForm):  # Create a admin user the first time the app is launched
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    password_confirmation = PasswordField("Répeter le mot de passe", validators=[EqualTo('password')])
    is_admin = BooleanField("Administrateur", default=False)
    submit = SubmitField("Créer")


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    cover_img = FileField("Cover Image", validators=[])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[])  # Could not use DataRequired because tinymce hide this field. Use POST validation.
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField('Save')


class TagForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
