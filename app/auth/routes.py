# Third party packages
from flask import request, session, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

# My modules
from . import auth_bp
from .validations import RegistrationForm, AuthentificationForm
from ..database import add_user, get_user_by_email


@auth_bp.route('/reg', methods=['GET', 'POST'])
def register():
    """Register new user"""

    # Form object for validations check
    form = RegistrationForm(request.form)

    # User already passed registration - full name in session
    if (request.method == 'GET') and (session.get('name') is not None):
        return redirect(url_for('chat.rooms'))

    # User is not passed registration - full name not in session
    elif (request.method == 'GET') and (session.get('name') is None):
        return render_template('reg.html', form=form)

    # User enter registration form - check validation
    elif request.method == 'POST' and form.validate():

        # Retrieve data from form
        email: str = form.email.data
        password: str = form.password.data
        full_name: str = form.full_name.data
        department: str = form.department.data
        department_role: str = form.department_role.data

        # Generate hash from entered password
        hashed_password = generate_password_hash(password)

        # Save entered data and hashed password to database
        add_res = add_user(email, hashed_password, full_name, department, department_role)

        # Error occured while adding user to database
        if add_res[0] is False:
            flash(add_res[1])
            return render_template('reg.html', form=form)
        else:
            # Save data to session if no error while adding user to database
            session['email'] = email
            session['name'] = full_name
            session['department'] = department
            session['department_role'] = department_role

            # Show all available chats to enter
            return redirect(url_for('chat.rooms'))

    # User entered registration form but validation error occured
    else:
        return render_template('reg.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authentificate user"""

    # Form object for validations check
    form = AuthentificationForm(request.form)

    # User already passed registration or authentification- full name in session
    if (request.method == 'GET') and (session.get('name') is not None):
        return redirect(url_for('chat.rooms'))

    # User is not passed registration or authentification - full name not in session
    elif (request.method == 'GET') and (session.get('name') is None):
        return render_template('login.html', form=form)

    # User enter authentification form - check validation
    elif (request.method == 'POST') and (form.validate()):

        # Retrieve data from form
        email: str = form.email.data
        password: str = form.password.data

        # Compare user data with database
        user = get_user_by_email(email)

        # Check if such user exist in database or no transaction error occured
        if len(user) <= 0 or user[0] is None:
            flash(f"No user with email {email}")
            return render_template('login.html', form=form)
        else:
            # Compare password in database with entered password
            if check_password_hash(user[0].password, password):

                # Save data from database to session
                session['email'] = user[0].email
                session['name'] = user[0].full_name
                session['department'] = user[0].department
                session['department_role'] = user[0].department_role

                return redirect(url_for('chat.rooms'))

            else:
                flash("Incorrect password")
                return render_template('login.html', form=form)
