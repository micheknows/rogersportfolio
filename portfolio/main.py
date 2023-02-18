from flask import Flask, render_template
from flask_login import LoginManager, login_required
from portfolio.models.portfolio import PortfolioItemDB
from portfolio.auth import auth_bp
from portfolio.auth import user_model

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = PortfolioItemDB()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return user_model.User.query.get(int(user_id))

@app.route("/")
def index():
    items = db.read_all()
    return render_template("index.html", items=items)

@app.route('/my_view')
@login_required
def my_view():
    # Your code here
    return render_template('my_template.html', context)

if __name__ == "__main__":
    app.run()
