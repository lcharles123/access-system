from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey
from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta
import re
import bcrypt


''' Represents admin, users, lock_users and locks
    Used for locks to have the same underlying security as regular users
    @schema: User(id(pk), username, name, email, password, created, role, authenticated)
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'user'
    # username can be 0 (admin), room number(4 digits), 
    # enrollment id(10 digits), user(#TODO check if there is a unique id in this case)
    username = db.Column('username', db.String(32), unique=True, nullable=False)
    @validates('username')
    def validate_username(self, key, username):
        value = None
        try:
            value = int(username)
        except:
            raise ValueError("username must be a integer.")
        else:
            if value == 0:
                return username
            elif len(username) <= 10 and value > 0:
                return username
            else:
                raise ValueError("'"+username+"' must be in the range: [0, 9999999999].")

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64))
    @validates('email')
    def validate_email(self, key, email): 
        email = email.lower()
        pattern = r'[a-z0-9_.-]+@[a-z0-9\-]+\.[a-z0-9\-.]+$'
        # email can be '' for lock
        if not re.match(pattern, email) and email != '':
            raise ValueError("Invalid email address: '"+email+"'")
        return email.lower()

    password = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String, nullable=False) # can be admin, user, lock, lock_user
    @validates('role')
    def validate_role(self, key, role):
        if role not in ['admin', 'user', 'lock', 'lock_user']:
            raise ValueError("Unknown role '"+role+"'")
        return role

    authenticated = db.Column(db.Boolean, default=False)
    
    # use username as fk in Entry_List and preserve them after deleting ref data
    #author_rel = db.relationship('Entry_List', backref='author_ref', cascade='all, delete-orphan', passive_deletes=True, foreign_keys=lambda: Entry_List.author(role='lock_user'))
    
    #room_rel = db.relationship('Entry_List', backref='room_ref', cascade='all, delete-orphan', passive_deletes=True, foreign_keys=lambda: Entry_List.room(role='lock'))
    
    # properties implemented in UserMixin
    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def what_role(self):
        return self.role
    
    ''' Row like object: 
        dict with key:value representing col_name:row_value
    '''
    @property
    def as_row(self):
        return self.__dict__


''' Permissions table, user room
    @schema: Permissions(room(fk), user(fk), created, key)
'''
class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'permissions'
    room = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    @validates('room')
    def validate_room(self, key, value):
        User.query.filter_by(username=value).first()
        return value
        user = User.query.filter_by(username=value).first()
        
        if user and user.role != 'lock':
            raise ValueError('room must be a user with user.role == lock')
        return value
        
    user = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    @validates('user')
    def validate_user(self, key, value):
        return value
        user = User.query.filter_by(username=value).first()
        if user and user.role != 'lock_user':
            raise ValueError('user must be a user with user.role == lock_user')
        return value

    created = db.Column(db.DateTime, default=datetime.utcnow)
    expires = db.Column(db.Boolean, default=False)
    # set as needed
    expiration_date = db.Column(db.DateTime, default=(datetime.utcnow() + timedelta(days=180)))
    
    key = db.Column(db.String(64)) #FIXME ajust as needed
    
    def get_username(self):
        return self.user
    
    def get_room(self):
        return self.room

    ''' Row like object: 
        dict with key:value representing col_name:row_value
    '''
    @property
    def as_row(self):
        return self.__dict__

''' List of users that used the locks
'''
class Entry_List(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'entry_list'
    
    #author = db.Column(db.Integer, db.ForeignKey('user.username', ondelete='SET NULL', onupdate='SET NULL', deferrable=True), nullable=True)
    
    #room = db.Column(db.Integer, db.ForeignKey('user.username', ondelete='SET NULL', onupdate='SET NULL', deferrable=True), nullable=True)
    room = db.Column(db.String(64), nullable=False) #FIXME ensures exists on User table
    @validates('room')
    def validate_room(self, key, value):
        User.query.filter_by(username=value, role='lock').first()
        if user == None:
            raise ValueError('room must be a user with user.role == lock')
        return value
    author = db.Column(db.String(64), nullable=False) #FIXME ensures exists on User table
    @validates('author')
    def validate_user(self, key, value):
        return value
        user = User.query.filter_by(username=value).first()
        if user and user.role != 'lock_user':
            raise ValueError('user must be a user with user.role == lock_user')
        return value

    date = db.Column(db.DateTime, default=datetime.utcnow)
    granted = db.Column(db.Boolean, nullable=False, default=False)
    
     # properties implemented in UserMixin
    def is_active(self):
        return True

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    ''' Row like object: 
        dict with key:value representing col_name:row_value
    '''
    @property
    def as_row(self):
        return self.__dict__
        
