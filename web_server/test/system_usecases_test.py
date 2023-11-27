# always use client to perform the following actions and check the showed tables.
# tests with a tipical usage of the system
# setup the system ina a env in production mode
# try enter a weak password and expect fail
# use a strong admin password with success
# using client, as admin, create users and locks
# login as a regular user and create 2  lock and 2 lock user
# a regular user will add a permission
# the system will check validty of the user in LDAP before adding
# your_flask_app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ...

# test_your_flask_app.py
import unittest
from your_flask_app import app, db, User

class YourAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_example(self):
        # Your test code here
        pass

if __name__ == '__main__':
    unittest.main()

# use #classmethod
import unittest
from your_flask_app import app, db

class YourAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_example_1(self):
        # Your test code here
        pass

    def test_example_2(self):
        # Your test code here
        pass

if __name__ == '__main__':
    unittest.main()

# the lock will send 1 request to enter the room
# the server will grant the permissions 
# the permission will be revoked
# the same user will try to enter the room without success

#check entrie tables if the requests are ok

