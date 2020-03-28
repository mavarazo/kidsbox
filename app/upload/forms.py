from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    music = FileField('Music', validators=[DataRequired()])
    submit = SubmitField('Upload')
