from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class SermonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    preacher = StringField('Preacher', validators=[DataRequired()])
    created_at = DateField('Date Preached', format='%Y-%m-%d')
    description = TextAreaField('Description')
    audio_file = FileField('Audio File', validators=[FileAllowed(['mp3', 'wav'], 'Audio only!'), DataRequired()])
    submit = SubmitField('Upload Sermon')
