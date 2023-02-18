from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for
from main import app, db, login_manager
from .models.portfolio import PortfolioItemDB
from .models.user_model import User

bp = Blueprint('main', __name__)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Try to find the user in the database
        user = User.query.filter_by(username=username).first()

        # If the user exists and the password is correct, log them in
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('portfolio'))
        else:
            # If the user doesn't exist or the password is incorrect, show an error message
            error = 'Invalid username or password.'
            return render_template('login.html', error=error)

    else:
        # If the request is GET, just show the login page
        return render_template('login.html')


@app.route('/portfolio')
@login_required
def portfolio():
    db = PortfolioItemDB()
    portfolio_items = db.read_all()
    return render_template('portfolio.html', portfolio_items=portfolio_items)


@app.route('/portfolio/new', methods=['GET', 'POST'])
@login_required
def new_portfolio_item():
    # Your code here to handle creating a new portfolio item
    return redirect(url_for('portfolio'))

@app.route('/portfolio/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio_item(item_id):
    # Your code here to handle editing an existing portfolio item
    return redirect(url_for('portfolio'))

@app.route('/portfolio/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_portfolio_item(item_id):
    # Your code here to handle deleting an existing portfolio item
    return redirect(url_for('portfolio'))

@bp.route('/')
def index():
    return render_template('index.html')
