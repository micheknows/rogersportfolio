# /portfolio/auth.py

from flask import Blueprint
auth = Blueprint('auth', __name__)

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Try to find the user in the database
        user = User.query.filter_by(username=username).first()

        # If the user exists and the password is correct, log them in
        if user and user.check_password(password):
            flash("Successfully logged in", category='success')
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            # If the user doesn't exist or the password is incorrect, show an error message
            error = 'Invalid username or password.'
            flash(error, category='error')
            return render_template('login.html')

    else:
        # If the request is GET, just show the login page
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

