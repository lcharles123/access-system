import unittest
from your_flask_app import create_app

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def tearDown(self):
        pass  # Optional cleanup after each test


def test_example(self):
    with self.app.test_request_context('/example'):
        # Test your route behavior here


def test_home_route(self):
    response = self.app.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Welcome', response.data)



def test_form_submission(self):
    response = self.app.post('/submit', data={'field1': 'value1', 'field2': 'value2'})
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Success', response.data)



# another way
from flask_testing import TestCase

class FlaskTest(TestCase):
    def create_app(self):
        return create_app()

    def test_example(self):
        response = self.client.get('/')
        self.assert200(response)


# database
class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.db = db  # Replace with your database instance

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

