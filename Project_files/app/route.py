
from flask import render_template, redirect, flash, url_for
from markupsafe import Markup
from sqlalchemy import text
import pandas as pd
from app import app
from utils.db_utils import get_db_connection
from models.customers import Customer
from app.forms import *

# Home Page
@app.route('/')
def index():

    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Shop Page
@app.route('/shop')
def shop():
    return render_template('shop.html')

# Shop Single/Product Page
@app.route('/shop-single')
def shop_single():
    return render_template('shop-single.html')

# Login Page
@app.route('/Login')
def login():

    form = LoginForm()
    signup_form = CustomerForm()
    return render_template('Login.html', signup_form=signup_form, form=form)
