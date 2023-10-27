from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from server.database import db
from flask_login import UserMixin
from datetime import datetime
import bcrypt
# used for user model, maybe its good to have for all models

''' Represents admin, users, lock_users and locks
    Used for locks to have the same underlying security as regular users
    @param ---
'''
class User(db.Model, UserMixin): #FIXME alter to SystemUser, because User can be a person wanting to access the lock
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    __tablename__ = 'user'
    # username can be 0, room number, enrollment id
    username = db.Column('username', db.String(32))
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True) 
    password = db.Column(db.String(64)) # hash sha256 alg
    created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String, default="user") # can be admin, user, lock, lock_user
    authenticated = db.Column(db.Boolean, default=False)
    
    # properties implemented in UserMixin
    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

''' Permissions table, can ingress in a room?
'''
class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'permissions'
    room = ForeignKey('user.username')
    user = ForeignKey('user.username')
    key = db.Column(db.String(64)) #FIXME ajust as needed
    
    def get_room(self):
        return self.room
    
    def get_key(self):
        return self.key

''' List of users that used the locks
'''
class Entry_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'entry_list'
    room = ForeignKey('user.username')
    author = ForeignKey('user.username')
    date = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=False)
    
    def get_enrollment(self):
        return self.author
    
    def get_room(self):
        return self.room
    
    
    
    
    
    
    

