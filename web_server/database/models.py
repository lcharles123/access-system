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


''' Permissions table with user and room
    @schema: Permissions(room(fk), user(fk), created, expires, expiration_date)
'''
class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'permissions'
    room_name = db.Column(db.String(64), nullable=False)
    @validates('room_name')
    def validate_room(self, key, value):
        user = User.query.filter_by(username=value, role='lock').first()
        if user == None:
            raise ValueError('Inexistent room with room.role == lock')
        else:
            return value
    room = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    @validates('room')
    def validate_room(self, key, value):
        user = User.query.filter_by(username=value, role='lock').first()
        if user == None:
            raise ValueError('Inexistent room with room.role == lock')
        else:
            return value
    user_name = db.Column(db.String(64), nullable=False)
    @validates('user_name')
    def validate_user(self, key, value):
        user = User.query.filter_by(username=value, role='lock_user').first()
        if user == None:
            raise ValueError('Inexistent author with author.role == lock_user')
        else:
            return value
    user = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    @validates('user')
    def validate_user(self, key, value):
        user = User.query.filter_by(username=value, role='lock_user').first()
        if user == None:
            raise ValueError('Inexistent user with user.role == lock_user')
        else:
            return value
    created = db.Column(db.DateTime, default=datetime.utcnow)
    expires = db.Column(db.Boolean, default=False)
    expiration_date = db.Column(db.DateTime, default=(datetime.utcnow() + timedelta(days=180)))
    
    ''' Row like object: 
        dict with key:value representing col_name:row_value
    '''
    @property
    def as_row(self):
        return self.__dict__

''' List of users that tried to activate the locks
'''
class Entry_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'entry_list'
    
    room_name = db.Column(db.String(64), nullable=False)
    @validates('room_name')
    def validate_room(self, key, value):
        user = User.query.filter_by(username=value, role='lock').first()
        if user == None:
            raise ValueError('Inexistent room with room.role == lock')
        else:
            return value
    room = db.Column(db.String(64), nullable=False)
    @validates('room')
    def validate_room(self, key, value):
        user = User.query.filter_by(username=value, role='lock').first()
        if user == None:
            raise ValueError('Inexistent room with room.role == lock')
        else:
            return value
    author_name = db.Column(db.String(64), nullable=False)
    @validates('author_name')
    def validate_user(self, key, value):
        user = User.query.filter_by(username=value, role='lock_user').first()
        if user == None:
            raise ValueError('Inexistent author with author.role == lock_user')
        else:
            return value
    author = db.Column(db.String(64), nullable=False)
    @validates('author')
    def validate_user(self, key, value):
        user = User.query.filter_by(username=value, role='lock_user').first()
        if user == None:
            raise ValueError('Inexistent author with author.role == lock_user')
        else:
            return value
    date = db.Column(db.DateTime, default=datetime.utcnow)
    granted = db.Column(db.Boolean, nullable=False, default=False)
    
    ''' Row like object: 
        dict with key:value representing col_name:row_value
    '''
    @property
    def as_row(self):
        return self.__dict__
        
