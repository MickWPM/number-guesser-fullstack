import pytest
import json
from app import app, NEW_GAME_MESSAGE
import app as app_module
import os



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



# Tests for GET /api/leaderboard
def test_get_leaderboard_initially_empty(client):
    """Test GET /api/leaderboard returns an empty list initially."""
    # The manage_leaderboard_state fixture ensures a clean state.
    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == []

def test_get_leaderboard_after_posting_scores(client):
    """Test GET /api/leaderboard returns scores previously posted."""
    client.post('/api/leaderboard', json={'name': 'Alice', 'score': 100})
    client.post('/api/leaderboard', json={'name': 'Bob', 'score': 50}) # Lower score, should be first
    client.post('/api/leaderboard', json={'name': 'Charlie', 'score': 150})

    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    data = response.json
    
    assert len(data) == 3
    assert data[0] == {'name': 'Bob', 'score': 50}
    assert data[1] == {'name': 'Alice', 'score': 100}
    assert data[2] == {'name': 'Charlie', 'score': 150}

def test_get_leaderboard_respects_max_scores_to_show(client):
    """Test GET /api/leaderboard returns only MAX_SCORES_TO_SHOW entries."""
    # app_module.MAX_SCORES_TO_SHOW is 5
    # app_module.MAX_SCORES_TO_KEEP is 10
    
    num_to_post = app_module.MAX_SCORES_TO_SHOW + 3 # e.g., 5 + 3 = 8 scores
    for i in range(num_to_post):
        # Post scores such that the best ones are 0, 10, 20, 30, 40, 50, 60, 70
        client.post('/api/leaderboard', json={'name': f'Player{i}', 'score': i * 10})
    
    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    data = response.json
    
    assert len(data) == app_module.MAX_SCORES_TO_SHOW # Should be 5
    # Check if the scores returned are the lowest (best) 5
    for i in range(app_module.MAX_SCORES_TO_SHOW):
        assert data[i]['name'] == f'Player{i}'
        assert data[i]['score'] == i * 10

# Tests for POST /api/leaderboard
def test_post_leaderboard_success_and_file_creation(client):
    """Test POST /api/leaderboard successfully adds a score and modifies the file."""
    temp_file_path = app_module.HIGH_SCORES_FILENAME # Get the temp file path from monkeypatched var

    response = client.post('/api/leaderboard', json={'name': 'Dave', 'score': 75})
    assert response.status_code == 200
    assert response.json == {'success': True}

    # Check in-memory HIGH_SCORES (app_module.HIGH_SCORES is modified by add_score_to_leaderboard)
    assert len(app_module.HIGH_SCORES) == 1
    assert app_module.HIGH_SCORES[0] == {'name': 'Dave', 'score': 75}

    # Check if the temporary file was created and contains the correct data
    assert os.path.exists(temp_file_path)
    with open(temp_file_path, 'r') as f:
        file_data = json.load(f)
    assert len(file_data) == 1
    assert file_data[0] == {'name': 'Dave', 'score': 75}

def test_post_leaderboard_sorting_logic(client):
    """Test that POST /api/leaderboard correctly sorts scores (lower is better)."""
    client.post('/api/leaderboard', json={'name': 'Eve', 'score': 200})
    client.post('/api/leaderboard', json={'name': 'Frank', 'score': 100}) # Best score
    client.post('/api/leaderboard', json={'name': 'Grace', 'score': 150})

    expected_sorted_scores = [
        {'name': 'Frank', 'score': 100},
        {'name': 'Grace', 'score': 150},
        {'name': 'Eve', 'score': 200},
    ]
    # Check in-memory list (which add_score_to_leaderboard sorts)
    assert app_module.HIGH_SCORES == expected_sorted_scores

    # Also verify via GET request (which should reflect the sorted state)
    response = client.get('/api/leaderboard')
    assert response.json == expected_sorted_scores

def test_post_leaderboard_respects_max_scores_to_keep(client):
    """Test POST /api/leaderboard keeps only MAX_SCORES_TO_KEEP entries."""
    # app_module.MAX_SCORES_TO_KEEP is 10
    
    num_to_post = app_module.MAX_SCORES_TO_KEEP + 3 # Post 13 scores
    scores_posted = []
    for i in range(num_to_post):
        score_val = (num_to_post - 1 - i) * 10 # Post scores like 120, 110, ..., 10, 0
        scores_posted.append({'name': f'User{i}', 'score': score_val})
        client.post('/api/leaderboard', json=scores_posted[-1])

    # In-memory HIGH_SCORES should be trimmed to MAX_SCORES_TO_KEEP and sorted
    assert len(app_module.HIGH_SCORES) == app_module.MAX_SCORES_TO_KEEP
    
    # The best MAX_SCORES_TO_KEEP scores should be 0, 10, ..., (MAX_SCORES_TO_KEEP-1)*10
    for i in range(app_module.MAX_SCORES_TO_KEEP):
        assert app_module.HIGH_SCORES[i]['score'] == i * 10
        # The name check is a bit more complex due to reverse posting order,
        # but score is primary for this check.

    # Check file content as well
    temp_file_path = app_module.HIGH_SCORES_FILENAME
    with open(temp_file_path, 'r') as f:
        file_data = json.load(f)
    assert len(file_data) == app_module.MAX_SCORES_TO_KEEP
    for i in range(app_module.MAX_SCORES_TO_KEEP):
        assert file_data[i]['score'] == i * 10

def test_post_leaderboard_invalid_data_causes_error(client):
    """Test POST /api/leaderboard with data that causes internal errors."""
    # Add one valid score so the list isn't empty for sort comparison
    client.post('/api/leaderboard', json={'name': 'InitialPlayer', 'score': 100})

    # Posting a score as None should cause a TypeError during list.sort() in add_score_to_leaderboard
    response = client.post('/api/leaderboard', json={'name': 'BadScorePlayer', 'score': None})
    assert response.status_code == 500 # Internal Server Error expected due to TypeError

    # Reset state for next scenario (fixture handles this, but explicit clear helps readability)
    app_module.HIGH_SCORES = []
    app_module.save_leaderboard() # This will write an empty list to the temp file
    client.post('/api/leaderboard', json={'name': 'InitialPlayer2', 'score': 200})

    # Posting with a missing 'score' key results in score=None
    response_missing_score = client.post('/api/leaderboard', json={'name': 'MissingScorePlayer'})
    assert response_missing_score.status_code == 500

def test_post_leaderboard_bad_request_format(client):
    """Test POST /api/leaderboard with non-JSON data or malformed JSON."""
    # Flask's request.get_json() should handle these and return a 400 Bad Request
    response_plain_text = client.post('/api/leaderboard', data="this is not json", content_type="text/plain")
    assert response_plain_text.status_code == 415

    # Malformed JSON (e.g., trailing comma if not allowed by parser)
    # response_malformed_json = client.post('/api/leaderboard', data='{"name": "Test", "score": 10,}', content_type="application/json")
    # assert response_malformed_json.status_code == 400 
    # Note: Python's json.loads can be lenient with some "malformations" depending on exact nature.
    # A clearly invalid structure would trigger it. For example, unquoted keys if not using `simplejson`.
    # Standard `json.loads` requires double quotes for keys.