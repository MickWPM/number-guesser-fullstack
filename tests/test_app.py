import pytest
import json
from app import app, NEW_GAME_MESSAGE

def test_home_page_responds(client):
    """('/') should return an ok status code: 200"""
    response = client.get('/')
    assert response.status_code == 200 

def test_new_game_api_returns_json_and_message(client):
    response = client.get('/api/new_game')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # response.data contains the response body as bytes.
    # For JSON, you can parse it using json.loads()
    # or use response.json if your Flask version/test client provides it directly.
    try:
        data = response.json # Tries to parse JSON directly
    except AttributeError: # Fallback for older versions or if .json isn't on test response
        data = json.loads(response.data.decode('utf-8'))
    
    assert 'message' in data
    assert NEW_GAME_MESSAGE in data['message']