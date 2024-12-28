from flask import flash, render_template, url_for, redirect
from markupsafe import Markup

from models.manager import Manager
from models.customers import Customer



def validate_signup(login_form, signup_form):

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
                login_form=login_form
            )

    # If form validation fails
    flash("Form validation failed. Please correct the errors and try again.", "warning")
    return render_template('Login.html', signup_form=signup_form, login_form=login_form)


def validate_login(login_form, signup_form):
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        # Check if the email exists in the database
        user1 = Customer.get_by_email(email)
        user2 = Manager.get_by_email(email)

        if user1 is None and user2 is None:
            flash("User not found. Please sign up for an account.", "warning")

            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=login_form
            )

        if user1 is not None and user1.passcode == password:
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        elif user1 is not None and user1.passcode != password:
            flash("Incorrect password. Please try again.", "danger")
            return render_template(
                'Login.html',
                signup_form=signup_form,
                login_form=login_form)

        if user2 is not None and user2.passcode == password:
            flash("Login successful!", "success")
            return redirect(url_for('index'))

        elif user2 is not None and user2.passcode != password:
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
