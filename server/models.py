from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin
# used for user model, maybe its good to have for all models

db = SQLAlchemy()

''' Represents a user.
    @param username 
    @param password

'''
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    __tablename__ = 'user'
    name = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True) #same as email
    password = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False



