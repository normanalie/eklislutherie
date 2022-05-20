import imghdr
import re

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, regexp


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    cover_img = FileField("Cover Image", validators=[])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField('Save')
    
    def check_image(cls, file):
        """
        Return a secure filename if image is correct. Otherwise return False.
        """
        # Check extension
        match = re.search('^$|([^\s]+(\.(?i)(jpe?g|png|gif|bmp))$)', file.filename)
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
