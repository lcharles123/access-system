import sys
sys.path.append('./../../')
from server.database import *
from conftest import *

def test_hello_index(client):
    response = client.get('/')
    assert response.status_code == 200

# Add more tests as needed
'''from app.models import User

def test_create_user(client, session):
    response = client.post('/create_user', json={'username': 'test_user'})
    assert response.status_code == 201

    user = session.query(User).filter_by(username='test_user').first()
    assert user is not None

# Add more tests as needed
'''
