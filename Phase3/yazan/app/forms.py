from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email

class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_signin = SubmitField('Sign In')
    submit_signup = SubmitField('Sign Up')