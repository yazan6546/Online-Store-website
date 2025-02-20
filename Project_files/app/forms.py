from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Regexp


class StrongPassword:
    def __init__(self, message=None):
        if not message:
            message = ('Password must contain at least one uppercase letter\n, one lowercase letter, one digit, '
                       'and one special character.\nand Password must be at least 8 characters long.')
        self.message = message

    def __call__(self, form, field):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        validator = Regexp(pattern, message=self.message)
        validator(form, field)


class CustomerForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "First Name", "class": "form-control"}
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Last Name", "class": "form-control"}
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email", "class": "form-control", "id": "signup_email"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Password", "class": "form-control", "id": "signup_password"}
    )

    # Radio field for user type
    user_type = RadioField(
        'What is your role?',
        choices=[('manager', 'Manager'), ('customer', 'Customer')],
        validators=[DataRequired()],
        render_kw={"class": "form-check"}  # Optional: Add styling class if needed
    )

    birth_date = DateField(
        'Birth Date',
        default=date(2000, 1, 1),  # Set a default value
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )


    manager_role = SelectField(
        'Manager Role',
        render_kw={"class": "form-control"},
        choices=[('Financial Manager', 'Financial Manager'),
                 ('Regional Manager', 'Regional Manager'),
                 ('Assistant Manager', 'Assistant Manager')],
        validators=[DataRequired()]
    )


    submit = SubmitField(
        'Sign up',
        render_kw={"class": "btn btn-primary"}
    )


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email", "class": "form-control", "id":"signin_email"}  # Placeholder and styling
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Password", "class": "form-control", "id":"signin_password"}  # Placeholder and styling
    )
    submit_signin = SubmitField(
        'Sign in',
        render_kw={"class": "btn btn-primary"}  # Button styling
    )
