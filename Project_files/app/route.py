
from flask import render_template, redirect, flash, url_for
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

    if login_form.validate_on_submit():
        pass

    if signup_form.validate_on_submit():
        return valid_signup(signup_form)

    return render_template('Login.html', signup_form=signup_form, login_form=login_form)

def valid_signup(signup_form):

    if signup_form.validate_on_submit():
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        email = signup_form.email.data
        password = signup_form.password.data
        user_type = signup_form.user_type.data

        # Create a new customer

        if user_type == 'manager'.lower():
            new_customer = Manager(first_name=first_name, last_name=last_name, email=email, passcode=password, since='2021-01-01')
        else:
            new_customer = Customer(first_name=first_name, last_name=last_name, email=email, passcode=password)

        if not new_customer.insert():
            print("Error inserting customer")
            flash(Markup('<strong>Success!</strong> Account created successfully!'), 'success')
            return redirect(url_for('login'))

    return render_template('Login.html', signup_form=signup_form, login_form=LoginForm())