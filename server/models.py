from flask_sqlalchemy import SQLAlchemy
from server.database import db
from flask_login import UserMixin
from datetime import datetime
# used for user model, maybe its good to have for all models

''' Represents admin, user, lock
'''

class Basic_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'
    username = db.Column(db.String(32))
    #email = db.Column(db.String(32), unique=True) 
    password = db.Column(db.String(64))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String, default="user") # can be admin, user, lock
    authenticated = db.Column(db.Boolean, default=False)

class Admin(Basic_User, UserMixin, extend_existing=True):
    email = db.Column(db.String(32), unique=True) 
    
    # properties implemented in UserMixin
    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

''' Represent permissions, store one enroll id for each person that can ingress in room
'''
class Permissions(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'room'
    name = db.Column(db.String(32))
    key = db.Column(db.String(16))

    def is_active(self):
        return True

    def get_name(self):
        return self.name

class Permissions(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'room'
    name = db.Column(db.String(32))
    key = db.Column(db.String(16))

    def is_active(self):
        return True

    def get_name(self):
        return self.name





