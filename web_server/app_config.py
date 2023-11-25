from os import urandom
''' Config file of flask app
    This is configured with classes, documentation here:
    https://flask.palletsprojects.com/en/2.3.x/config/
    
    
'''

class Config:
    DEBUG = False

class Production(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/database.sqlite"

class Development(Config):
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/foo.db"
    DEBUG = True
    SECRET_KEY = urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True
    MAX_CONTENT_LENGTH = None
    # ensure https
    #SESSION_COOKIE_SECURE = False

class Testing(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
