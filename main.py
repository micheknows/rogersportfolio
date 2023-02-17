from flask import Flask, render_template
from models.portfolio import PortfolioItem, PortfolioItemDB
from flask_login import LoginManager, login_required

from .auth import auth_bp

app.register_blueprint(auth_bp)


app = Flask(__name__)

# Initialize the database
db = PortfolioItemDB()

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'mysecretkey'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



@app.route("/")
def index():
    # Retrieve all portfolio items from the database
    items = db.get_all_items()

    # Render the template with the portfolio items
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run()
