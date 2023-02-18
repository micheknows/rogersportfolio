from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from portfolio import routes

from utils.database import db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import bp
    app.register_blueprint(routes.bp)

    return app
