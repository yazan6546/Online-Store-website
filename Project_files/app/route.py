
from flask import render_template, redirect, flash, url_for, request
from markupsafe import Markup

from app import app
from app.forms import *
from models.customers import Customer
from models.manager import Manager



# Home Page
@app.route('/')
def index():

    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Shop Page
@app.route('/shop')
def shop():
    return render_template('shop.html')

# Shop Single/Product Page
@app.route('/shop-single')
def shop_single():
    return render_template('shop-single.html')

# Login Page
@app.route('/Login', methods=['GET', 'POST'])
def login():

    signup_form = CustomerForm()
    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit() and 'submit_login' in request.form.keys():
        return redirect(url_for('login'))  # Possible redirection after login logic

    elif request.method == 'POST' and signup_form.validate_on_submit() and 'submit_signup' in request.form.keys():
        return valid_signup(signup_form)

    return render_template('Login.html', signup_form=signup_form, login_form=login_form)



def valid_signup(signup_form):
    if signup_form.validate_on_submit():  # Check if the form data is valid
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        email = signup_form.email.data
        password = signup_form.password.data
        user_type = signup_form.user_type.data

        # Create a new customer object
        if user_type.lower() == 'manager':  # Ensure case insensitivity
            new_customer = Manager(
                first_name=first_name,
                last_name=last_name,
                email=email,
                passcode=password,
                since='2021-01-01'
            )
        else:  # Regular customer
            new_customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                passcode=password
            )

        try:
            # Attempt to insert the new user into the database
            new_customer.insert()
            flash(
                Markup('<strong>Success!</strong> Account created successfully!'),
                'success'
            )

            return redirect(url_for('login'))  # Redirect to the login page
        except Exception as e:  # Handle MySQL IntegrityError (e.g., duplicate email)

            # Check if the exception is specifically for the duplicate email
            if "Duplicate entry" in str(e.orig):
                flash("Email already exists. Please use a different email address.", "danger")
            else:
                flash("An unexpected error occurred while creating your account. Please try again.", "danger")
            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=LoginForm()
            )

    # If form validation fails
    flash("Form validation failed. Please correct the errors and try again.", "warning")
    return render_template('Login.html', signup_form=signup_form, login_form=LoginForm())
