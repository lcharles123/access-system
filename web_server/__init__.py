from flask import Flask

from flask_login import LoginManager
from os import urandom, path
from .api.routes import generate_api_routes
from .database import db, db_init


def create_app():
    app = Flask(__name__)
    
    app.config['ENV'] = 'development'
    # let werkzeuk deal with debug messages
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = urandom(12)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MAX_CONTENT_LENGTH'] = None
    # ensure https
    app.config['SESSION_COOKIE_SECURE'] = False
    
    generate_api_routes(app) # from api.routes
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
#    if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
#        db.app = app
#        db.drop_all()
#        db.create_all()
#        if not db_init.create_admin_user():
#            raise Exception("create_admin_user failed")
    
    from .database.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    
    
    return app


