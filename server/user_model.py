from flask.ext.sqlalchemy import SQLAlchemy
#from . import db

db = SQLAlchemy()

''' Represents a user.
    @param username 
    @param password

'''
class User(db.Model):
    __tablename__ = 'user'
    
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

from . import db

