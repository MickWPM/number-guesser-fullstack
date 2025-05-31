import pytest
import json
from app import app

def test_guess_api_with_valid_guess(client):
    client.get('/api/new_game')

    guess_payload = {'guess':5}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    
    assert 'feedback' in data
    assert 'attempts_count' in data
    assert 'game_over' in data

    assert data['attempts_count'] == 1

def test_guess_api_with_non_int_guess(client):
    client.get('/api/new_game')

    guess_payload = {'guess':'5'}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 400

def test_guess_api_with_no_guess(client):
    client.get('/api/new_game')

    guess_payload = {}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 400

def test_guess_api_with_high_guess(game_with_known_secret):
    client = game_with_known_secret["client"]
    known_secret = game_with_known_secret["secret_number"]
    mock_randint = game_with_known_secret["mock_randint"] # Get the mock object

    client.get('/api/new_game')
    guess = known_secret + 1
    guess_payload = {'guess':guess}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    
    assert data['game_over'] == False

def test_guess_api_with_low_guess(game_with_known_secret):
    client = game_with_known_secret["client"]
    known_secret = game_with_known_secret["secret_number"]
    mock_randint = game_with_known_secret["mock_randint"] # Get the mock object

    client.get('/api/new_game')
    guess = known_secret - 1
    guess_payload = {'guess':guess}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    
    assert data['game_over'] == False

    
def test_guess_api_with_correct_guess(game_with_known_secret):
    client = game_with_known_secret["client"]
    known_secret = game_with_known_secret["secret_number"]
    mock_randint = game_with_known_secret["mock_randint"] # Get the mock object

    client.get('/api/new_game')
    guess_payload = {'guess':known_secret}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    
    assert data['game_over'] == True

    
def test_guess_api_with_multiple_guesses(client):
    client.get('/api/new_game')
    guess = -1
    
    guess_payload = {'guess':guess}
    response = client.post('/api/guess', json=guess_payload)

    guess_payload = {'guess':guess}
    response = client.post('/api/guess', json=guess_payload)

    guess_payload = {'guess':guess}
    response = client.post('/api/guess', json=guess_payload)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.json
    
    assert data['attempts_count'] == 3


