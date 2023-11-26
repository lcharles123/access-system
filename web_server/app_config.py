from os import urandom


''' Config file of flask app
    This is configured with classes, documentation here:
    https://flask.palletsprojects.com/en/2.3.x/config/
'''

class Config:
    DEBUG = False
    SECRET_KEY = urandom(12)
    # dict_like to overwrite on Production mode
    # This one is just for development
    ADMIN_EMAIL = 'admin@example.com' 
    # ADMIN_PASSWD in plain is not good aproach, but the easy-to-ingress one
    ADMIN_PASSWD = '123'
    FLASK_RUN_RELOADER = False

class Production(Config):
    
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = False
    MAX_CONTENT_LENGTH = None #FIXME put a aproximate value here, bytes
    SERVER_NAME = "localhost:6000"
    # ensure https
    SESSION_COOKIE_SECURE = True
    ADMIN_EMAIL = 'admin@example.com' 
    ADMIN_PASSWD = '123'


class Development(Config):
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/foo.db"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True
    MAX_CONTENT_LENGTH = None
    SERVER_NAME = "localhost:5000"
    SESSION_COOKIE_SECURE = False

class Testing(Development):
    DATABASE_URI = "sqlite:///:memory:"
    

