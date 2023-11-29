from .models import *
from . import db
from bcrypt import gensalt, hashpw
from datetime import datetime, timedelta


def get_user(username):
    return User.query.filter_by(username=username).first()

''' Insert user in db
    @param db: database object
    @param role: string in ['admin', 'user', 'lock', 'lock_user']
    @param atributes: dict like with {User.atributes : value}
    @return True if inserted, False otherwise
    @except ValueError when input data are incorrect
    # The exception trowing here is important to guarante a transparent inserting
'''
def insert_user(db, role, atributes={}):
    # check required atributes
    user = None
    try:
        if atributes['username'] == '' or \
           atributes['password'] == '':
            raise Exception()
    except:
        raise ValueError("'username' and 'password' required for all users.")
    if role == 'admin' or atributes['username'] == '0':
        if atributes['username'] != '0' or role != 'admin':
            return False 
        atributes['name'] = 'Admin'
        try:
            if atributes['email'] == '':
                raise Exception()
        except:
            raise ValueError("Email required for admin user.")
    elif role in ['user', 'lock', 'lock_user']:
        try:
            if role == 'lock_user' and len(atributes['username']) != 10:
                return False
            if role == 'lock' and len(atributes['username']) != 4:
                return False
            
            if atributes['name'] == '':
                raise Exception()
        except:
            raise ValueError("Name required for user lock and lock_user.")
    else:
        raise ValueError("'role' must be one of ['admin', 'user', 'lock', 'lock_user']")
    
    user = User.query.filter_by(username=atributes['username']).first()
    if user is None:
        email = ''
        try: email = atributes['email']
        except: pass
        user = User(username=atributes['username'], 
                    name=atributes['name'], 
                    email=email, 
                    password=hashpw(str(atributes['password']).encode(), gensalt()), 
                    role=role)
        db.session.add(user)
        db.session.commit()
        return get_user(atributes['username']) != None
    else:
        return False

def remove_user(db, username):
    user = get_user(username)
    if user != None and user.role != 'admin' and username != '0':    
        db.session.delete(user)
        db.session.commit()
        return get_user(username) == None
    else:
        return False

def get_all_table_users(role):
    return User.query.filter_by(role=role).all()

def is_valid_user(username, role):
    return User.query.filter_by(username=username, role=role).first() is not None

''' Operations perfomed on Entry_List
    Checks for roles are made in Permissions model class
    Expect a exception from this function if roles mismatch
'''
def set_permission(db, room, user):
    p = Permissions.query.filter_by(room=room, user=user).first()
    if p is None:
        p = Permissions(room=room, user=user)
        db.session.add(p)
        db.session.commit()
        return True
    else:
        return False

def revoke_permission(db, room, user):
    p = Permissions.query.filter_by(room=room, user=user).first()
    if p is not None:
        db.session.delete(p)
        db.session.commit()
        return True
    else:
        return False

def check_permission(db, room, user):
    return Permissions.query.filter_by(room=room, user=user).first() is not None

def get_permission_table():
    return Permissions.query.all()
    

''' Operations perfomed on Entry_List
    This table is insert_only and clear old than x days from now
'''
def insert_entry_list(db, room, username, granted):
    # checks(room, username) roles are made in model definition
    entry = Entry_List.query.filter_by(room=room, author=username).first()
    if entry is None:
        try:
            entry = Entry_List( room=room,
                                author=username,
                                granted=granted)
        except: 
            return False
        db.session.add(entry)
        db.session.commit()
        return True
    else:
        return False

def get_entry_table():
    return Entry_List.query.all()

''' For deleting all entries, only system admin can do it
'''
def clear_entry_list(db, do_backup_path=''):
    Entry_List.query.delete()
    return Entry_List.query.all().count() == 0

