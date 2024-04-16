import pytest

from flask import Flask
from backend.app import app





@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_vote(client):
    response = client.post('/vote', data={'option': 'Option 1', 'num_votes': '5'})
    assert response.status_code == 302  # Redirect status code

def test_invalid_vote(client):
    response = client.post('/vote', data={'option': 'B', 'num_votes': 'invalid'})
    assert b'Invalid number of votes' in response.data

