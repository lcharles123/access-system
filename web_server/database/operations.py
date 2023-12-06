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
    print(user)
    #raise Exception()
    return True
    if user == None:
        print('entrou')
        raise Exception()
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
    try:
        room_name = User.query.filter_by(username=room, role='lock').first()
        user_name = User.query.filter_by(username=user, role='lock_user').first()
        p = Permissions.query.filter_by(room=room, user=user).first()
        if p is None and room_name is not None and user_name is not None:
            p = Permissions(room=room, 
                            room_name=room_name.name, 
                            user=user,
                            user_name=user_name.name)
            db.session.add(p)
            db.session.commit()
            return True
        else:
            return False
    except:
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

def get_permission_table(room=None):
    if room is None:
        return Permissions.query.all()
    else:
        return Permissions.query.filter_by(room=room).all()
    

''' Operations perfomed on Entry_List
    This table is insert_only and clear old than x days from now
'''
def insert_entry_list(db, room, author, granted):
    lock_user = User.query.filter_by(username=author, role='lock_user').first()
    lock = User.query.filter_by(username=room, role='lock').first()
    
    entry = Entry_List.query.filter_by(room=room, author=author).first()
    if entry is None:
        try:
            entry = Entry_List( room=room,
                                room_name=lock.name,
                                author=author,
                                author_name=lock_user.name,
                                granted=granted)
        except: 
            return False
        db.session.add(entry)
        db.session.commit()
        return True
    else:
        return False

''' Get entry table by default
    @param on can be 'room' or 'user'
    it is used to filter the entries by room or user
'''
def get_entry_table(on=None, element=None):
    result = []
    if on == 'author':
        result = Entry_List.query.filter_by(author=element).all()
    elif on == 'room':
        result = Entry_List.query.filter_by(room=element).all()
    else:
        result = Entry_List.query.all()
    return result


''' For deleting all entries, only system admin can do it
'''
def clear_entry_list(do_backup_path=''):
    Entry_List.query.delete()
    return len(Entry_List.query.all()) == 0

