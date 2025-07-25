
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class MemberForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[Optional()])
    membership_status = SelectField('Membership Status', choices=[
        ('Baptised', 'Baptised'), 
        ('Not Baptised', 'Not Baptised'), 
        ('Visitor', 'Visitor')], default='Visitor')
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
