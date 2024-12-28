
from flask import render_template, request
from app import app
from app.forms import *
import app.auth as auth




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

    if 'submit_login' in request.form.keys():
        return auth.validate_login(login_form, signup_form)  # Possible redirection after login logic

    elif'submit_signup' in request.form.keys():
        return auth.validate_signup(login_form, signup_form)

    return render_template('Login.html', signup_form=signup_form, login_form=login_form)