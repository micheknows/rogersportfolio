#!/usr/bin/env python3.9

# /portfolio/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from markupsafe import Markup


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lkajgakdjl;gjasdfkjlakjsdfj'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://micheknows:ph0nics3@localhost/portfolio'

    @app.template_filter('reverse')
    def reverse_filter(s):
        if s:
            return s[::-1]
        else:
            return s

    app.jinja_env.filters['reverse'] = reverse_filter


    db.init_app(app)

    # just forcing a commit


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
