import unittest
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from flask.ctx import AppContext
from web_server.database.models import User, Permissions, Entry_List  # Replace with the actual module name
from web_server.database import db
from web_server.database import operations as op
from web_server import app_config

class Test_Database_Models(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        db.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    def tearDown(self):
        self.session.rollback()
        self.session.close()
    # auxiliary functions
    def aux_add_commit(self, user):
        self.session.add(user)
        self.session.commit()
    
    def test_can_create_admin_user(self):
        user = User(username='0', email='admin@example.com', name='admin', role='admin', password='123')
        self.aux_add_commit(user)
        
        user1 = self.session.query(User).filter_by(username='0').first()
        self.assertIsNotNone(user1)
        self.assertEqual(user1.role, 'admin')
        self.assertEqual(user1.email, 'admin@example.com')
    
    def test_not_nullable_user_field_username(self):
        with self.assertRaises(Exception):
            user = User(email='admin@example.com', name='admin', role='admin', password='123')
            self.aux_add_commit(user)
    
    def test_nullable_user_field_email(self):
        try:
            user = User(username='0', name='admin', role='admin', password='123')
            self.aux_add_commit(user)
        except:
            self.fail("email can be null")
    
    def test_not_nullable_user_field_name(self):
        user = User(username='0', email='admin@example.com', role='admin', password='123')
        with self.assertRaises(Exception):
            self.aux_add_commit(user)
    
    def test_not_nullable_user_field_role(self):
        user = User(username='0', email='admin@example.com', name='admin', password='123')
        with self.assertRaises(Exception):
            self.aux_add_commit(user)
    
    def test_not_nullable_user_field_password(self):
        user = User(username='0', email='admin@example.com', name='admin', role='admin')
        with self.assertRaises(Exception):
            self.aux_add_commit(user)
    
    def test_not_nullable_entry_list_author(self):
        null_author = Entry_List(room='1111', author=None)
        with self.assertRaises(Exception):
            self.aux_add_commit(null_author)

    def test_not_nullable_entry_list_room(self):
        null_room = Entry_List(room=None, author='1111223333')
        with self.assertRaises(Exception):
            self.aux_add_commit(null_room)

    def test_not_raises_creation_entry_list_entry(self):
        try:
            not_null = Entry_List(room='1111', author='1111223333')
            self.aux_add_commit(not_null)
        except:
            self.fail("room and author should be not null")
    
    def test_username_validation_positive(self):
        with self.assertRaises(Exception):
            User(username='-1', name='lock1', role='lock', password='123')
    
    def test_username_validation1(self):
        with self.assertRaises(Exception):
            User(username='10000000000', 
                 name='user1', email='user1@example.com', 
                 role='lock_user', password='123')
    
    def test_username_must_be_unique(self):
        user1 = User(username='0', email='admin@example.com', name='admin', role='admin', password='123')
        user1_again = User(username='0', email='admin@example.com', name='admin', role='admin', password='123')
        self.aux_add_commit(user1)
        with self.assertRaises(Exception):
            self.aux_add_commit(user1_again)
        
    def test_email_validation(self):
        with self.assertRaises(Exception):
            User(username='0', email='adminexample.com', name='admin', role='admin', password='123')
    
    def test_role_validation(self):
        try:
            User(username='0', email='admin@example.com', name='admin1', role='admin', password='123')
            User(username='1', email='1@example.com', name='user1', role='user', password='123')
            User(username='2', email='2@example.com', name='lock1', role='lock', password='123')
            User(username='3', email='3@example.com', name='lock_user1', role='lock_user', password='123')
        except:
            self.fail("User role(s) correct, but validation wrong")
    
    def test_can_create_and_delete_regular_user(self):
        user = User(username='1', email='1@example.com', name='1', role='user', password='123')
        self.aux_add_commit(user)
        user1 = self.session.query(User).filter_by(username='1').first()
        
        self.assertIsNotNone(user1)
        self.assertEqual(user1.role, 'user')
        self.assertEqual(user1.email, '1@example.com')
        
        self.assertEqual(self.session.query(User).count(), 1) 
        self.session.delete(user1)
        self.assertEqual(self.session.query(User).count(), 0) 
    
    def test_can_create_and_delete_locks(self):
        user = User(username='1111', name='lock1', role='lock', password='123')
        self.aux_add_commit(user)
        user1 = self.session.query(User).filter_by(username='1111').first()
        
        self.assertIsNotNone(user1)
        self.assertEqual(user1.role, 'lock')
        self.assertIsNone(user1.email)
        
        self.assertEqual(self.session.query(User).count(), 1) 
        self.session.delete(user1)
        self.assertEqual(self.session.query(User).count(), 0)

    def test_can_create_and_delete_lock_users(self):
        user = User(username='1234121234', name='user1', role='lock_user', password='123')
        self.aux_add_commit(user)
        user1 = self.session.query(User).filter_by(username='1234121234').first()
        
        self.assertIsNotNone(user1)
        self.assertEqual(user1.role, 'lock_user')
        self.assertIsNone(user1.email)
        
        self.assertEqual(self.session.query(User).count(), 1) 
        self.session.delete(user1)
        self.assertEqual(self.session.query(User).count(), 0)

    def test_can_create_and_delete_entry_list(self):
        entry = Entry_List(room='1234', author='1234001234', granted=True)
        self.aux_add_commit(entry)
        entry1 = self.session.query(Entry_List).filter_by(room='1234', author='1234001234').first()
        
        self.assertIsNotNone(entry1)
        self.assertTrue(entry1.granted)
        
        self.assertEqual(self.session.query(User).count(), 1) 
        self.session.delete(user1)
        self.assertEqual(self.session.query(User).count(), 0)

'''
        # Create test users
        user1 = User(username='user1', name='User 1', email='user1@example.com', password='password1')
        user2 = User(username='user2', name='User 2', email='user2@example.com', password='password2')

        self.session.add_all([user1, user2])
        self.session.commit()

        # Insert permissions
        permissions = Permissions(username_1='user1', username_2='user2')
        self.session.add(permissions)
        self.session.commit()

        # Check if permissions are inserted correctly
        self.assertEqual(self.session.query(Permissions).count(), 1)
'''
class Test_Database_Operations(unittest.TestCase):
    def setUp(self):
        from flask import Flask
        self.app = Flask(__name__)
        self.app.config.from_object(config_type())
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    '''def test_permissions_inserting(self):
        # Create test users
        user1 = User(username='user1', name='User 1', email='user1@example.com', password='password1')
        user2 = User(username='user2', name='User 2', email='user2@example.com', password='password2')

        self.session.add_all([user1, user2])
        self.session.commit()

        # Insert permissions
        permissions = Permissions(username_1='user1', username_2='user2')
        self.session.add(permissions)
        self.session.commit()

        # Check if permissions are inserted correctly
        self.assertEqual(self.session.query(Permissions).count(), 1)'''

    def test_get_user(self):
        pass

    def test_insert_and_cannot_remove_admin_user(self):
        pass

    def test_insert_and_remove_regular_user(self):
        pass

    def test_insert_and_remove_lock_user(self):
        pass

    def test_insert_and_remove_lock_user_user(self):
        pass

    def test_set_permission_from_user_to_lock_and_check_them(self):
        pass

    def test_try_setting_permissions_and_failing_for_incompatible_roles(self):
        pass

    def test_get_all_table_users(self):
        pass

    def test_set_and_revoke_permission(self):
        pass

    def test_get_permission_table(self):
        pass

    def test_insert_entry_list(self):
        pass

    def test_can_not_insert_entry_list_incompatible_roles(self):
        pass
    def test_get_entry_table(self):

        pass

    def test_clear_entry_list(self):
        pass

    def test_validate_room_as_user_model_in_permissions_table(self):
        pass

    def test_validate_author_as_user_model_in_permissions_table(self):
        pass

    def test_validate_entries_in_entry_table(self):
        pass

'''
def get_user(username):
    return User.query.filter_by(username=username).first()

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

def remove_user(db, username):
    user = get_user(username)
    if user is not None:
        if user.role == 'admin' or username == '0':
            raise ValueError("Can not remove 'admin' user.")
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False

def get_all_table_users(role):
    return User.query.filter_by(role=role).all()
def is_valid_user(username, role):
    return User.query.filter_by(username=username, role=role).first() is not None


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
    


def insert_entry_list(db, room, username, success):
    # checks(room, username) roles are made in model definition
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
    # Add similar test methods for removing and purging permissions, and for Entry_List operations
    ''''''
class Test_Database_Sched_Operations(unittest.TestCase):
    
    
    def test_clear_database_older_than_x_days(self):
        pass

    def test_revoke_permissions_with_expiration_date(self):
        pass'''

if __name__ == '__main__':
    unittest.main()

