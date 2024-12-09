from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Regexp


class StrongPassword:
    def __init__(self, message=None):
        if not message:
            message = 'Password must contain at least one uppercase letter\n, one lowercase letter, one digit, and one special character.\nand Password must be at least 8 characters long.'
        self.message = message

    def __call__(self, form, field):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        validator = Regexp(pattern, message=self.message)
        validator(form, field)

class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), StrongPassword()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_signin = SubmitField('Sign In')
    submit_signup = SubmitField('Sign Up')