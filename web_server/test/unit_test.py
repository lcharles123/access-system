import unittest
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from flask.ctx import AppContext
from web_server.database.models import User, Permissions, Entry_List
from web_server.database import db
from web_server.database import operations as op
from bcrypt import checkpw 
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
    # auxiliary function
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

class Test_Database_Operations_User(unittest.TestCase):
    def setUp(self):
        from flask import Flask
        self.app = Flask(__name__)
        self.app.config.from_object(app_config.Testing())
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.session = db.session()
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_get_user(self):
        userattr={'username': '1235', 
                   'email': 'someuser@example.com', 
                   'name': 'user1',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'user', atributes=userattr))
            self.assertTrue(op.get_user('1235'))
        
    def test_insert_and_cannot_remove_admin_user(self):
        # ensured admin is username == 0
        admin_user={'username': '0', 
                   'email': 'admin@example.com', 
                   'name': 'Admin',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'admin', atributes=admin_user))
            self.assertFalse(op.remove_user(db, '0'))
            
    def test_passwords_hashed_using_bcrypt_hashpw(self):
        admin_user={'username': '0', 
                   'email': 'admin@example.com', 
                   'name': 'Admin',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'admin', atributes=admin_user))
            user = op.get_user('0')
            self.assertTrue(checkpw(('123').encode(), user.password))
    
    def test_insert_and_cannot_have_more_than_one_admin(self):
        admin_user={'username': '0', 
                   'email': 'adm4in@example.com', 
                   'name': 'Ad4min',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'admin', atributes=admin_user))
            self.assertFalse(op.insert_user(db, 'admin', atributes=admin_user))

    def test_can_not_insert_other_user_as_admin(self):
        other_user={'username': '2020001234',
                    'email': 'admin@example.com', 
                    'name': 'other user',
                    'password':'123'}
        with self.app.app_context():
            self.assertFalse(op.insert_user(db, 'admin', atributes=other_user))
            
    def test_can_not_insert_admin_as_other_user(self):
        admin_user={'username': '0', 
                  'email': 'admin@example.com', 
                  'name': 'Admin',
                  'password':'123'}
        with self.app.app_context():
            self.assertFalse(op.insert_user(db, 'lock_user', atributes=admin_user))
            self.assertFalse(op.insert_user(db, 'user', atributes=admin_user))
            self.assertFalse(op.insert_user(db, 'lock', atributes=admin_user))
    
    def test_can_not_insert_lock_user_as_admin_or_lock(self):
        # assuming username of lock_user is 10 char len
        # admin is 1 char len
        # lock is 4 char len
        lock_user={'username': '2020001234', 
                  'email': 'user1@example.com', 
                  'name': 'User1',
                  'password':'123'}
        with self.app.app_context():
            self.assertFalse(op.insert_user(db, 'admin', atributes=lock_user))
            self.assertFalse(op.insert_user(db, 'lock', atributes=lock_user))
    
    def test_insert_and_remove_lock(self):
        lock={'username': '1233', 
                   'email': 'lock1@example.com', 
                   'name': 'lock1',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'lock', atributes=lock))
            self.assertTrue(op.get_user('1233'))
            self.assertTrue(op.remove_user(db, '1233'))
            self.assertFalse(op.get_user('1233'))

    def test_insert_and_remove_lock_user(self):
        lock_user={'username': '2020001234', 
                   'email': 'user1@example.com', 
                   'name': 'user1',
                   'password':'123'}
        with self.app.app_context():
            self.assertTrue(op.insert_user(db, 'lock_user', atributes=lock_user))
            self.assertTrue(op.get_user('2020001234'))
            self.assertTrue(op.remove_user(db, '2020001234'))
            self.assertFalse(op.get_user('2020001234'))
    
    def test_can_create_and_delete_lock_users(self):
        user = User(username='1234121234', name='user1', role='lock_user', password='123')
        self.session.add(user)
        self.session.commit()
        user1 = self.session.query(User).filter_by(username='1234121234').first()
        
        self.assertIsNotNone(user1)
        self.assertEqual(user.role, 'lock_user')
        self.assertIsNone(user.email)
        
        self.assertEqual(self.session.query(User).count(), 1) 
        with self.app.app_context():
            self.session.delete(user1)
        self.assertEqual(self.session.query(User).count(), 0)

    def test_not_nullable_entry_list_author(self):
        with self.app.app_context():
            null_author = Entry_List(room='1111', author=None)
            with self.assertRaises(Exception):
                self.aux_add_commit(null_author)
    
    def test_not_nullable_entry_list_room(self):
        with self.app.app_context():
            null_room = Entry_List(room=None, author='1111223333')
            with self.assertRaises(Exception):
                self.aux_add_commit(null_room)
    
    def test_raises_creation_entry_list_entry_wieh_user_not_existent(self):
        with self.assertRaises(Exception): 
            not_null = Entry_List(room='1111', author=None)
            
    def test_not_nullable_entry_list_author(self):
        with self.assertRaises(Exception):
            Entry_List(room='1111', author=None)
    
    def test_not_nullable_entry_list_room(self):
        with self.assertRaises(Exception):
            Entry_List(room=None, author='1111223333')


class Test_Database_Operations_Permission_And_Entry_List(unittest.TestCase):
    # here setup will populate the table with one user each
    def setUp(self):
        from flask import Flask
        self.app = Flask(__name__)
        self.app.config.from_object(app_config.Testing())
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            one_admin = User(username='0', name='Admin', 
                    email='admin@example.com', password='123', role='admin')
            one_user = User(username='100099', name='', 
                    email='admin1@example.com', password='123', role='user')
            one_lock = User(username='1111', name='1111 lab1', 
                    email='email1111@example.com', password='123', role='lock')
            two_lock = User(username='2222', name='2222 lab', 
                    email='email2222@example.com', password='123', role='lock')
            one_lock_user = User(username='2020001111', name='Lock User1', 
                    email='LockUser1@example.com', password='123', role='lock_user')
            two_lock_user = User(username='2020002222', name='Lock User old', 
                    email='User@example.com', password='123', role='lock_user')
            db.session.add_all([one_admin, one_user, one_lock, two_lock, one_lock_user, two_lock_user])
            db.session.commit()
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_set_permission_from_user_to_lock_and_check_them(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '1111', '2020001111'))
            self.assertEqual(len(op.get_permission_table()), 1)
            self.assertTrue(op.check_permission(db, '1111', '2020001111'))
            
    def test_try_setting_permissions_and_failing_for_incompatible_roles(self):
        with self.app.app_context():
            self.assertFalse(op.set_permission(db, '2222', '100099'))
            self.assertFalse(op.set_permission(db, '2222', '2222'))
            self.assertFalse(op.set_permission(db, '2020001111', '2020002222'))
            self.assertFalse(op.set_permission(db, '2020002222', '2222'))
            self.assertEqual(len(op.get_permission_table()), 0)

    def test_set_and_revoke_permission(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '2222', '2020002222'))
            self.assertEqual(len(op.get_permission_table()), 1)
            self.assertTrue(op.revoke_permission(db, '2222', '2020002222'))
            self.assertFalse(op.check_permission(db, '2222', '2020002222'))
            self.assertEqual(len(op.get_permission_table()), 0)

    def test_get_permission_table(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '1111', '2020001111'))
            self.assertTrue(op.set_permission(db, '1111', '2020002222'))
            self.assertFalse(op.set_permission(db, '9999', '2020002222'))
            self.assertFalse(op.set_permission(db, '1111', '2020002222'))
            self.assertEqual(len(op.get_permission_table()), 2)

    def test_validate_entries_in_entry_table(self):
        with self.app.app_context():
            self.assertFalse(op.insert_entry_list(db, '2345', '2020002222', True))
            self.assertEqual(len(op.get_permission_table()), 0)

    def test_validate_room_in_permissions_table(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '1111', '2020002222'))
            self.assertFalse(op.set_permission(db, '2020001111', '2020002222'))
            self.assertFalse(op.set_permission(db, 'sdfgdfsdfg', '2020002222'))
            self.assertFalse(op.set_permission(db, '7777', '2020001111'))
            self.assertEqual(len(op.get_permission_table()), 1)
            
    def test_validate_author_in_permissions_table(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '1111', '2020002222'))
            self.assertFalse(op.set_permission(db, '9999', '2020002222'))
            self.assertFalse(op.set_permission(db, '1111', 'asdfasdf'))
            self.assertEqual(len(op.get_permission_table()), 1)
    
    def test_get_all_permission_table_users(self):
        with self.app.app_context():
            self.assertTrue(op.set_permission(db, '2222', '2020002222'))
            self.assertTrue(op.set_permission(db, '1111', '2020002222'))
            self.assertTrue(op.set_permission(db, '1111', '2020001111'))
            self.assertEqual(len(op.get_permission_table()), 3)

    def test_insert_entry_list(self):
        with self.app.app_context():
            self.assertTrue(op.insert_entry_list(db, '2222', '2020001111', True))
            self.assertFalse(op.insert_entry_list(db, '2020001111', '2344', False))
            self.assertFalse(op.insert_entry_list(db, '1111', '2020009999', True))
            self.assertEqual(len(op.get_entry_table()), 1)
    
    def test_check_granted_entry_list(self):
        with self.app.app_context():
            self.assertTrue(op.insert_entry_list(db, '2222', '2020001111', True))
            self.assertTrue(op.get_entry_table()[0].granted)
            
    def test_check_denied_entry_list(self):
        with self.app.app_context():
            self.assertTrue(op.insert_entry_list(db, '2222', '2020001111', False))
            self.assertFalse(op.get_entry_table()[0].granted)
    
    def test_get_entry_table(self):
        with self.app.app_context():
            self.assertTrue(op.insert_entry_list(db, '2222', '2020002222', True))
            self.assertTrue(op.insert_entry_list(db, '1111', '2020002222', False))
            self.assertTrue(op.insert_entry_list(db, '1111', '2020001111', True))
            self.assertEqual(len(op.get_entry_table()), 3)
    
    def test_clear_entry_list(self):
        with self.app.app_context():
            self.assertTrue(op.clear_entry_list())
            self.assertEqual(len(op.get_entry_table()), 0)


if __name__ == '__main__':
    unittest.main()

