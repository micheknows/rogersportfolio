from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from flask import Blueprint
from .models import user_model  # import the User model


# create a new blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# add the login route to the auth blueprint
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_ = user_model.User.get_by_username(username)

        if user_ and user_.check_password(password):
            login_user(user_)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')
