from flask import Flask

from flask_login import LoginManager
from password_strength import PasswordPolicy
import logging
from os import urandom, path
from .api.routes import generate_api_routes
from .database import db, db_init
from .database.operations import insert_user
from .database.models import User
from . import app_config

''' Configure and create the web app
    Need to specify a config class constructor
'''
def create_app(development=True):
    config_type = None
    if development:
        config_type=app_config.Development
    else:
        config_type=app_config.Production
    app = Flask(__name__)
    app.config.from_object(config_type())
    generate_api_routes(app) # from api.routes
    db.init_app(app)
    db.app = app
    with app.app_context():
        # do production thing
        # atributes for each branch below
        passwd = str(app.config['ADMIN_PASSWD'])
        email = str(app.config['ADMIN_EMAIL'])
        atributes={'username': '0', 
               'email': email, 
               'password': passwd}
        result = False
        if app.config['ENV'] == 'production': 
            db.create_all()
            # code to add admin
            strong_pass = PasswordPolicy.from_names(
            length=8,  # Requires all assigned here...
            uppercase=1,
            numbers=1,
            special=1)
            if not strong_pass.test(passwd):
                raise ValueError("Admin password too weak. \
                Define a 8 char length, and some upper, lower case,\
                 number and a special char in the app_config.py file")
            result = insert_user(db, 'admin', atributes=atributes)
        else:
            db.drop_all()
            db.create_all()
            result = insert_user(db, 'admin', atributes=atributes)
        if result:
            print("Admin was set now.")
        else:
            print("Admin already set, doing nothing.")
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

