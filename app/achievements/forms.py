from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, MultipleFileField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    cover_img = FileField("Cover Image", validators=[])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[])  # Could not use DataRequired because tinymce hide this field. Use POST validation.
    tags = SelectMultipleField("Tags", coerce=int)
    images = MultipleFileField('Images', validators=[])
    submit = SubmitField('Save')

