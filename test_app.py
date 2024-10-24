# test_app.py

import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add(client):
    response = client.get('/add')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['result'] == 5  # Check the result of 2 + 3

def test_subtract(client):
    response = client.get('/subtract')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['result'] == 3  # Check the result of 5 - 2
