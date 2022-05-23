from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TagForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
