
from flask import render_template, request, jsonify, session, flash, redirect, url_for
from wtforms.validators import email

from app import app
from app.forms import *
import app.auth as auth
from models.addresses import Address
from models.customers import Customer
from models.manager import Manager
from models.suppliers import Supplier
from models.products import Product




app.first_request_handled = False

#
# @app.before_request
# def handle_first_request():
#     if not app.first_request_handled:
#         print("This is the first request. Clearing session.")
#         session.clear()  # Clear the session for the first request only
#         app.first_request_handled = True  # Set the flag so it doesn't run again
#


# Route for the Administrator Dashboard

############################################################################################################
# Customers section
############################################################################################################

# Route for the Specialists page
@app.route('/admin_dashboard/customers')
def admin_dashboard_customers():

    if 'user' not in session.keys() or session.get('role') != 'manager':
        flash("You must be logged in as manager to access the admin dashboard.", "warning")
        return redirect(url_for('login'))

    customers = Customer.get_all()
    customers = [customer.to_dict(address=True) for customer in customers]

    #print(customers[0]['addresses'][0]['address_id'])
    return render_template('customers.html', customers=customers)  # Replace with render_template if applicable


@app.route('/edit_customer/<int:person_id>', methods=['POST'])
def edit_customer(person_id):
    # Logic to update the customer with the given person_id
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    customer = Customer.get(person_id)
    customer.first_name = first_name
    customer.last_name = last_name
    customer.update()
    return redirect(url_for('admin_dashboard_customers'))


@app.route('/delete_customer/<int:person_id>', methods=['POST'])
def delete_customer(person_id):
    # Logic to delete the customer with the given person_id
    result = Customer.delete(person_id)
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Customer not found"})


@app.route('/update_customer/<int:person_id>', methods=['POST'])
def update_customer(person_id):
    # Logic to update the customer with the given person_id
    customer = Customer.get(person_id)

    customer.first_name = request.form['first_name']
    customer.last_name = request.form['last_name']
    customer.email = request.form['email']

    result = customer.update()

    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "An error occurred while updating the customer"})

@app.route('/search_customer', methods=['GET'])
def search_customer():

    name = request.args.get('query')

    customers = Customer.search(name)
    if customers or customers==[]:
        customers = [customer.to_dict(address=True) for customer in customers]
        return jsonify({"success": True, "customers": customers})

    return jsonify({"success": False, "error": "An error occurred while searching for customers"})

@app.route('/filter_customers', methods=['GET'])
def filter_customers():
    # Dummy customer data to return
    customers = [
        {"person_id": 1, "addresses": "123 Oak Street, Springfield"},
        {"person_id": 2, "addresses": "456 Maple Avenue, Shelbyville"},
        {"person_id": 3, "addresses": "789 Pine Road, Capital City"},
        {"person_id": 4, "addresses": "321 Birch Lane, Ogdenville"},
        {"person_id": 5, "addresses": "654 Cedar Street, North Haverbrook"}
    ]
    return jsonify({"success": True, "customers": customers})

############################################################################################################
# Managers Section
############################################################################################################


# Route for the managers page
@app.route('/admin_dashboard/managers')
def admin_dashboard_managers():

    if 'user' not in session.keys() or session.get('role') != 'manager':
        flash("You must be logged in as manager to access the admin dashboard.", "warning")
        return redirect(url_for('login'))

    managers = Manager.get_all()
    managers = [manager.to_dict() for manager in managers]

    return render_template('managers.html', managers=managers)  # Replace with render_template if applicable



@app.route('/delete_manager/<int:person_id>', methods=['POST'])
def delete_manager(person_id):
    # Logic to delete the customer with the given person_id

    if session['user']['person_id'] == person_id:
        return jsonify({"success": False, "error": "You cannot delete yourself."})

    result = Manager.delete(person_id)
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Manager not found"})


@app.route('/update_manager/<int:person_id>', methods=['POST'])
def update_manager(person_id):
    # Logic to update the customer with the given person_id

    manager = Manager.get(person_id)

    print(manager)

    manager.first_name = request.form['first_name']
    manager.last_name = request.form['last_name']
    manager.email = request.form['email']
    manager.role = request.form['role']

    result = manager.update()

    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "An error occurred while updating the customer"})

@app.route('/search_manager', methods=['GET'])
def search_manager():

    name = request.args.get('query')

    managers = Manager.search(name)

    if managers or managers==[]:
        managers = [manager.to_dict() for manager in managers]
        return jsonify({"success": True, "managers": managers})

    return jsonify({"success": False, "error": "An error occurred while searching for managers"})


############################################################################################################
# suppliers section
############################################################################################################
@app.route('/admin_dashboard/suppliers')
def admin_dashboard_suppliers():
    if 'user' not in session.keys() or session.get('role') != 'manager':
        flash("You must be logged in as manager to access the admin dashboard.", "warning")
        return redirect(url_for('login'))

    suppliers = Supplier.get_all()
    suppliers = [supplier.to_dict() for supplier in suppliers]

    return render_template('suppliers.html', suppliers=suppliers)

    return "<h1>Supplier Page</h1>"  # Replace with render_template if applicable

# update
@app.route('/update_supplier/<int:supplier_id>', methods=['POST'])
def update_supplier(supplier_id):
    try:
        # Extract data from the request
        name = request.form.get('name')
        phone = request.form.get('phone')

        # Validate inputs
        if not name or not phone:
            return jsonify(success=False, error="Name and phone are required.")

        # Fetch the supplier by ID and update its fields
        supplier = Supplier.get_by_supplier_id(supplier_id)
        if not supplier:
            return jsonify(success=False, error="Supplier not found.")

        supplier.name = name
        supplier.phone = phone
        result = supplier.update()

        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Failed to update supplier.")
    except Exception as e:
        return jsonify(success=False, error=str(e))

# Delete
@app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    try:
        # Call the delete method of the Supplier class
        result = Supplier.delete(supplier_id)

        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Failed to delete supplier from that database")
    except Exception as e:
        return jsonify(success=False, error=str(e))

# search
@app.route('/search_supplier', methods=['GET'])
def search_supplier():
    try:
        # Get the search query from the request
        query = request.args.get('query', '')

        # Fetch all suppliers and filter them by name or phone
        all_suppliers = Supplier.get_all()
        filtered_suppliers = [
            supplier.to_dict() for supplier in all_suppliers
            if query.lower() in supplier.name.lower() or query in supplier.phone
        ]

        return jsonify(success=True, suppliers=filtered_suppliers)
    except Exception as e:
        return jsonify(success=False, error=str(e))

# get all suppliers
@app.route('/get_suppliers', methods=['GET'])
def get_suppliers():
    try:
        # Use the get_all class method of the Supplier class
        suppliers = Supplier.get_all()
        suppliers_dicts = [supplier.to_dict() for supplier in suppliers]

        return jsonify(success=True, suppliers=suppliers_dicts)
    except Exception as e:
        return jsonify(success=False, error=str(e))

# add supplier
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    try:
        # Extract data from the request
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')

        # Validate inputs
        if not name or not phone:
            return jsonify(success=False, error="Name and phone are required.")

        # Create and insert a new supplier
        new_supplier = Supplier(supplier_name=name, phone_number=phone)
        new_supplier.insert()

        return jsonify(success=True, supplier=new_supplier.to_dict())
    except Exception as e:
        return jsonify(success=False, error=str(e))


############################################################################################################
#Category section
############################################################################################################

# Route for the Parents page
@app.route('/admin_dashboard/categories')
def admin_dashboard_categories():
    return "<h1>Categories Page</h1>"  # Replace with render_template if applicable


############################################################################################################
# Statistics section
############################################################################################################

# Route for the Organization Statistics (Report) page
@app.route('/organization_statistics')
def organization_statistics():
    return "<h1>Organization Statistics Page</h1>"  # Replace with render_template if applicable

############################################################################################################
# Products section
############################################################################################################

# Route for the Register Parent and Child page
@app.route('/admin_dashboard/products')
def admin_dashboard_products():
    return "<h1>Products page</h1>"  # Replace with render_template if applicable

############################################################################################################
# Customer's orders section
############################################################################################################

# Route for the Payments page
@app.route('/admin_dashboard/customer_orders')
def admin_dashboard_customer_orders():
    return "<h1>customer's orders</h1>"  # Replace with render_template if applicable



############################################################################################################
# Manager's orders section
############################################################################################################

@app.route('/admin_dashboard/managers_orders')
def admin_dashboard_managers_orders():
    return "<h1>manager's orders</h1>"  # Replace with render_template if applicable


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

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():

    if 'user' not in session.keys() or session.get('role') != 'manager':
        flash("You must be logged in as manager to access the admin dashboard.", "warning")
        print('ok loser')
        return redirect(url_for('login'))


    admin = session['user']
    return render_template('admin_dashboard.html', admin=admin)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    customer_form = CustomerForm()
    print(customer_form.first_name.data)
    print(request.method)
    if customer_form.validate_on_submit():
        first_name = customer_form.first_name.data
        last_name = customer_form.last_name.data
        email = customer_form.email.data
        passcode = customer_form.password.data

        print("ok")
        customer = Customer(first_name=first_name, last_name=last_name, email=email, passcode=passcode, hash=True)
        customer.insert()
        return redirect(url_for('admin_dashboard_customers'))
    else:
        print(customer_form.form_errors)
        return render_template('add_customer.html', form=customer_form)


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


@app.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    # Logic to delete the address with the given address_id
    result = Address.delete(address_id)
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "An error occured while deleting the address."})

@app.route('/edit_address/<int:address_id>', methods=['POST'])
def edit_address(address_id):
    # Logic to update the address with the given address_id
    street = request.form['street']
    city = request.form['city']
    zip_code = request.form['zip_code']

    address = Address.get(address_id)

    print(address)

    address.street = street
    address.city = city
    address.zip_code = zip_code
    result = address.update(address_id)

    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "An error occurred while updating the address."})



@app.route("/orders")
def get_orders():
    orders = [
        {"order_id": 1, "product": "Laptop", "quantity": 1, "price": 1200.00},
        {"order_id": 2, "product": "Headphones", "quantity": 2, "price": 150.00}
    ]
    return jsonify({"orders": orders})

