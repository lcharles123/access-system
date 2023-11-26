from flask import Flask

from flask_login import LoginManager
from os import urandom, path
from .api.routes import generate_api_routes
from .database import db, db_init
from .database.models import User
from . import app_config

''' Configure and create the web app
'''
def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config.Development())
    
    generate_api_routes(app) # from api.routes

    db.init_app(app)
    db.app = app
    with app.app_context():
        db.create_all()  
        u = User.query.filter_by(username='0').first()
        if u == None:
            from bcrypt import hashpw, gensalt
            from password_strength import PasswordPolicy
            strong_pass = PasswordPolicy.from_names(
            length=8,  # Requires all assigned here...
            uppercase=1,
            numbers=1,
            special=1)
            passwd = app.config['ADMIN_PASSWD']
            env = app.config['ENV']
            if env == 'production' and not strong_pass.test(passwd):
                raise ValueError("Admin password too weak. \
                Define a 8 char length, and some upper, lower case,\
                 number and a special char")
            admin = User(username='0', 
                         name='Admin', 
                         email=app.config['ADMIN_EMAIL'], 
                         password=hashpw(str(app.config['ADMIN_PASSWD']).encode(), gensalt()), 
                         role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin was set now.")
        else:
            print("Admin already set, doing nothing.")
    print(User.query.all()[0].__dict__)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
#        db.app = app
#        db.drop_all()
#        db.create_all()
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

