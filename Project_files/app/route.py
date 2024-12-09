from flask import render_template, redirect, flash, url_for
from markupsafe import Markup
from sqlalchemy import text
import pandas as pd
from app import app
from app.db_utils import get_db_connection
from app.forms import *

@app.route('/')
@app.route('/index')
def index():
    connection = get_db_connection()
    query = "SELECT * FROM Store.Customer"
    df = pd.read_sql(query, connection)
    connection.close()
    customers_html = df.to_html(classes='customers-table', index=False)
    return render_template('index.html', title='Home', customers_table=Markup(customers_html))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.submit_signup.data)
    print(form.validate_on_submit())
    if form.submit_signup.data:
        return redirect(url_for('signup'))
    elif form.submit_signin.data and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Store.Customer WHERE Customer.email=%s AND Customer.password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:

            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CustomerForm()
    if form.validate_on_submit():
        # Handle form submission, e.g., save to database

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        add_customer_data(first_name, last_name, email, password)

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

def add_customer_data(first_name, last_name, email, password):
    connection = get_db_connection()
    query = text('INSERT INTO Store.Customer (first_name, last_name, email, password) '
            'VALUES (:first_name, :last_name, :email, :password)')

    connection.execute(query, {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password}
                       )
    connection.commit()  # Commit the transaction
    connection.close()