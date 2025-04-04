from datetime import datetime

from flask import flash, render_template, url_for, redirect, session
from markupsafe import Markup
import utils.password_manager as pm
from models.cart import Cart
from models.manager import Manager
from models.customers import Customer



def validate_signup(login_form, signup_form):

    if signup_form.validate_on_submit():  # Check if the form data is valid
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        email = signup_form.email.data
        password = signup_form.password.data
        user_type = signup_form.user_type.data
        birth_date = signup_form.birth_date.data
        print(birth_date)

        print(type(birth_date))

        try:
            # Create a new customer object
            if user_type.lower() == 'manager':
                role = signup_form.manager_role.data

                new_customer = Manager(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    passcode=password,
                    since=datetime.now(),
                    role=role,
                    hash=True
                )
            else:
                # Regular customer
                new_customer = Customer(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    passcode=password,
                    birth_date=signup_form.birth_date.data,
                    hash=True
                )

                # Attempt to insert the new user into the database
            new_customer.insert()
            flash(
                Markup('<strong>Success!</strong> Account created successfully!'),
                'success'
            )

            return redirect(url_for('login'))  # Redirect to the login page
        except Exception as e:

            # Handle MySQL IntegrityError (e.g., duplicate email)

            # Check if the exception is specifically for the duplicate email
            if "Duplicate entry" in str(e):
                print("okok")
                flash("Email already exists. Please use a different email address.", "danger")
            else:
                print("okok11")
                flash(str(e), "danger")

            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=login_form
            )

    else:
        for field, errors in signup_form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(signup_form, field).label.text}: {error}", "danger")
        flash("An error occured with the form. Try again.", "danger")
        return render_template('Login.html', signup_form=signup_form, login_form=login_form)


def validate_login(login_form, signup_form):
    if login_form.validate_on_submit():


        email = login_form.email.data
        password = login_form.password.data

        # Check if the email exists in the database
        user1 = Customer.get_by_email(email)
        user2 = Manager.get_by_email(email)

        print(user1, user2)

        if user1 is None and user2 is None:
            flash("User not found. Please sign up for an account.", "warning")
            print("test")
            return redirect(url_for('login'))

        if user1 is not None and pm.verify_password(password, user1.passcode):
            flash("Login successful!", "success")
            print("ok error here")
            session['user'] = user1.to_dict()
            session['cart'] = Cart().to_dict()
            session['role'] = 'customer'
            print("ok error her2")
            return redirect(url_for('customer'))

        elif user1 is not None and not pm.verify_password(password, user1.passcode):
            flash("Incorrect password. Please try again.", "danger")
            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=login_form)

        if user2 is not None and pm.verify_password(password, user2.passcode):
            flash("Login successful!", "success")
            print("ok error her1")
            session['user'] = user2.to_dict()
            session['cart'] = Cart().to_dict()
            session['role'] = 'manager'
            print("ok error her2")
            return redirect(url_for('admin_dashboard'))

        elif user2 is not None and not pm.verify_password(password, user2.passcode):
            flash("Incorrect password. Please try again.", "danger")
            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=login_form)

        flash("An unexpected error occurred while logging in. Please try again.", "danger")


        return render_template(
            'Login.html',
            signup_form=signup_form,
            login_form=login_form
        )

    else:
        flash("Wrong email address entered. Try again.", "danger")
        return render_template('Login.html', signup_form=signup_form, login_form=login_form)
