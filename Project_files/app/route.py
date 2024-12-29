
from flask import render_template, request, jsonify, session, flash, redirect, url_for
from app import app
from app.forms import *
import app.auth as auth
from models.customers import Customer
from models.manager import Manager


app.first_request_handled = False


@app.before_request
def handle_first_request():
    if not app.first_request_handled:
        print("This is the first request. Clearing session.")
        session.clear()  # Clear the session for the first request only
        app.first_request_handled = True  # Set the flag so it doesn't run again



# Route for the Administrator Dashboard


# Route for the Specialists page
@app.route('/specialists')
def specialists():
    return "<h1>Specialists Page</h1>"  # Replace with render_template if applicable


# Route for the Children page
@app.route('/children')
def children():
    return "<h1>Children Page</h1>"  # Replace with render_template if applicable


# Route for the Courses page
@app.route('/courses')
def courses():
    return "<h1>Courses Page</h1>"  # Replace with render_template if applicable


# Route for the Parents page
@app.route('/parents')
def parents():
    return "<h1>Parents Page</h1>"  # Replace with render_template if applicable


# Route for the Organization Statistics (Report) page
@app.route('/organization_statistics')
def organization_statistics():
    return "<h1>Organization Statistics Page</h1>"  # Replace with render_template if applicable


# Route for the Register Parent and Child page
@app.route('/add_parent_and_child')
def add_parent_and_child():
    return "<h1>Register Parent and Child Page</h1>"  # Replace with render_template if applicable


# Route for the Payments page
@app.route('/payments')
def payments():
    return "<h1>Payments Page</h1>"  # Replace with render_template if applicable


# Route for logging out
@app.route('/logout')
def logout():
    return redirect(url_for('admin_dashboard'))  # Replace with your actual logout implementation


if __name__ == '__main__':
    app.run(debug=True)




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


@app.route('/customer')
def customer():
    if 'user' not in session.keys() or session.get('role') != 'customer':
        flash("You must be logged in as customer to access the customer dashboard.", "warning")
        return redirect(url_for('login'))

    return render_template('customer_dashboard.html')


@app.route('/admin_dashboard')
def admin_dashboard():

    if 'user' not in session.keys() or session.get('role') != 'manager':
        flash("You must be logged in as manager to access the admin dashboard.", "warning")
        print('ok loser')
        return redirect(url_for('login'))


    print(session['user'])
    admin = {'name': 'John Doe'}  # Example dictionary or an object

    return render_template('admin_dashboard.html', admin=admin)

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


@app.route("/orders")
def get_orders():
    orders = [
        {"order_id": 1, "product": "Laptop", "quantity": 1, "price": 1200.00},
        {"order_id": 2, "product": "Headphones", "quantity": 2, "price": 150.00}
    ]
    return jsonify({"orders": orders})

