import pytest
import sys

sys.path.append('.')
from app import app as appyFlat

@pytest.fixture
def app():
    app = appyFlat
    return app

@pytest.fixture
def client():
    app = appyFlat
    client = app.test_client()
    yield client
