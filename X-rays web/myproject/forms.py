from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,SelectField,TextAreaField,HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import ValidationError
from myproject.models import User


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone_number = StringField('Phone number',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must match !')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    birth_day = DateField('Birth Date', format = '%Y-%m-%d',validators = [DataRequired()])
    gender = SelectField('Gender', choices =['Male','Female'], validators= [DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Register!')
    
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password', message='Password does not match!')])
    submit = SubmitField('Change Password')
    
class SaveDiagnosisForm(FlaskForm):
    diagnosis_name = HiddenField('Diagnosis Name', validators=[DataRequired()])
    diagnosis_image = HiddenField('Diagnosis Image', validators=[DataRequired()])
    submit = SubmitField('Save Diagnosis')
    
    
    
    