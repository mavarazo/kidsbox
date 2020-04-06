from flask_wtf import FlaskForm

from wtforms import (
    FileField, 
    SelectField, 
    StringField, 
    SubmitField
)

from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    uid = StringField('UID')
    name = StringField('Name', validators=[DataRequired()])
    path = SelectField('Path', validators=[DataRequired()])
    artwork = FileField('Artwork')
    submit = SubmitField('Save')
