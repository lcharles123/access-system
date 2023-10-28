from server.database.models import *

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
            raise ValueError("Name required for lock and lock_user.")
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
                    password=atributes['password'], 
                    role=role).first()
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

def get_all_users(db, role):
    return User.query.filter_by(role=role).all()

def is_valid_user(db, username):
    return User.query.filter_by(username=username).first() is not None

def check_roles(room, user):
    # admin user is not valid as user of a room
   if room.role not in ['lock'] or user.role not in ['user, user_lock']:
        raise ValueError("Roles mismatch.") 
def set_permission(db, room, user):
    check_roles(room, user)
    p = Permissions.query.filter_by(room=room, user=user).first()
    if p is None:
        p = Permissions(room=room, user=user).first()
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

def insert_entry_list(db, room, user, success):
    check_roles(room, user)
    entry = Entry_list.query.filter_by(room=room, author=username).first()
    if entry is None:
        entry = Entry_list( room=room,
                            author=user,
                            success=success).first()
        db.session.add(entry)
        db.session.commit()
        return True
    else:
        return False

def clear_entry_list(db, do_backup_path=''):
    return Entry_List.query.delete()

