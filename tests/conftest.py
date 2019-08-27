import pytest
import sys

sys.path.append('.')
from app import app as colocApp

@pytest.fixture
def app():
    app = colocApp
    return app

@pytest.fixture
def client():
    app = colocApp
    client = app.test_client()
    yield client
