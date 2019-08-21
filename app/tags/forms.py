from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    uid = StringField('UID')
    name = StringField('Name', validators=[DataRequired()])
    path = SelectField('Path', validators=[DataRequired()])
    submit = SubmitField('Save')
