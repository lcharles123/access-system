from .models import *
from bcrypt import gensalt, hashpw

''' Insert user in db
    @param db: database object
    @param role: string among ['admin', 'user', 'lock', 'lock_user']
    @param atributes: dict like with {User.atributes : value}
    @return True if inserted, False otherwise
    @except ValueError when input data are incorrect
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
    if role == 'admin' or 'username' == '0':
        atributes['username'] = '0'
        atributes['name'] = 'admin'
        try:
            if atributes['email'] == '':
                raise Exception()
        except:
            raise ValueError("Email required for admin user.")
    elif role in ['user', 'lock', 'lock_user']:
        try:
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
        return True
    else:
        return False

def remove_user(db, role, username):
    if role == 'admin' or username == '0':
        raise ValueError("Can not remove 'admin' user.")
    user = User.query.filter_by(username=username).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False

def update_user(db, username, atributes):
    if role == 'admin' or username == '0':
        raise ValueError("Can not update 'admin' user.")
    #TODO: get_user(), user.atributes with atributes, insert_user()

def get_user(db, username):
    return User.query.filter_by(username=username).first()

def get_all_table_users(db, role):
    return User.query.filter_by(role=role).all()

def is_valid_user(db, username, role):
    return User.query.filter_by(username=username, role=role).first() is not None

def check_roles(room, user):
    room = User.query.filter_by(username=room).first()
    user = User.query.filter_by(username=user).first()
    if room is None or user is None:
        raise ValueError("Empty Roles")
    if room.role is 'lock' and user.role in ['lock_user', 'user']:
        raise ValueError("Roles mismatch: "+ user.role +" can't enter "+room.role)
            

def set_permission(db, room, user):
    check_roles(room, user)
    p = Permissions.query.filter_by(room=room, user=user).first()
    if p is None:
        p = Permissions(room=room, user=user)
        db.session.add(p)
        db.session.commit()
        return True
    else:
        return False

def revoke_permission(db, room, user):
    check_roles(room, user)
    p = Permissions.query.filter_by(room=room, user=user).first()
    if p is not None:
        db.session.delete(p)
        db.session.commit()
        return True
    else:
        return False

def check_permission(db, room, user):
    check_roles(room, user)
    return Permissions.query.filter_by(room=room, user=user).first() is not None

def get_permission_table():
    return Permissions.query.all()

def insert_entry_list(db, room, username, success):
    check_roles(room, username)
    entry = Entry_List.query.filter_by(room=room, author=username).first()
    if entry is None:
        entry = Entry_List( room=room,
                            author=username,
                            success=success)
        db.session.add(entry)
        db.session.commit()
        return True
    else:
        return False

def get_entry_table():
    return Entry_List.query.all()

def clear_entry_list(db, do_backup_path=''):
    return Entry_List.query.delete()

