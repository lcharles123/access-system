import pytest
import sys
sys.path.append('./../../')
from server.database import *

from server import create_app
app = create_app()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    with app.app_context():
        db.drop_all()

@pytest.fixture
def session(client):
    return db.session



