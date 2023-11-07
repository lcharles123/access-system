from flask import Flask

from flask_login import LoginManager
from os import urandom, path
from server.api.routes import generate_api_routes
from server.database import db, db_init


def create_app():
    app = Flask(__name__)
    
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = urandom(12)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
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
    
    from server.database.models import User

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

#flask run --cert adhoc for auto signed
'''
if __name__ == "__main__":
    app = create_app()
    #app.run(ssl_context=("cert.pem", "key.pem")) #TODO point it to keys
    app.run()'''
#create a self signed and configure on the command line, can be used to deploy too
#openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
#flask run --cert=cert.pem --key=key.pem
#app.run(port=5000, debug=True, host='localhost', use_reloader=True)

