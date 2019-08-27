import pytest
import sys

sys.path.append('.')
from app import app 

@pytest.fixture
def app():
    run_app = app.run(host='0.0.0.0', port=5000)
    return run_app

@pytest.fixture
def client():
    run_app = app.run(host='0.0.0.0', port=5000)
    client = app.test_client()
    yield client
