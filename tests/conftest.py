import pytest
import json
from app import app, NEW_GAME_MESSAGE, MIN_NUMBER, MAX_NUMBER
from unittest.mock import patch
import app as app_module

@pytest.fixture
def client():
    # Optional: Configure your app for testing.
    # This can disable error catching during request handling
    # so that you get better error reports when testing views.
    # It can also affect how some extensions behave.
    # app.config['TESTING'] = True
    # app.config['DEBUG'] = False # Ensure debug is off for more realistic testing if needed
    with app.test_client() as client_instance:
        yield client_instance
    # Any code after 'yield' would serve as teardown for this fixture.
    # For the basic Flask test client, explicit teardown is often not required here.

@pytest.fixture
def game_with_known_secret(client): # This new fixture uses the 'client' fixture
    """
    Sets up a game where the secret number is known.
    It mocks random.randint, starts a new game, and yields the client,
    the known secret number, and the mock object itself.
    """
    KNOWN_SECRET_NUMBER = 5  # Choose any consistent number for your tests

    # Use 'patch' as a context manager within the fixture.
    # This ensures the mock is active only during the scope of this fixture's use.
    with patch('app.random.randint') as mock_randint_instance:
        # Configure the mock to always return your KNOWN_SECRET_NUMBER
        mock_randint_instance.return_value = KNOWN_SECRET_NUMBER
        
        # Call /api/new_game to initialize the game in the app.
        # The app's call to random.randint will now use the mock.
        response_new_game = client.get('/api/new_game')
        assert response_new_game.status_code == 200 # Ensure new game started successfully
        
        # Yield whatever the tests will need. A dictionary is a good way to pass multiple values.
        yield {
            "client": client,
            "secret_number": KNOWN_SECRET_NUMBER,
            "mock_randint": mock_randint_instance # So tests can make assertions on the mock if needed
        }
        # The 'patch' context manager automatically cleans up the mock when this fixture's scope ends


@pytest.fixture(autouse=True)
def manage_leaderboard_state(tmp_path, monkeypatch):
    """
    Fixture to manage the leaderboard file and HIGH_SCORES state for each test.
    - Uses a temporary file for the leaderboard.
    - Resets the in-memory HIGH_SCORES list.
    - Calls load_leaderboard() to ensure a consistent starting state.
    """
    temp_leaderboard_file = tmp_path / "test_leaderboard.json"
    
    # Monkeypatch the app's global constant for the filename
    monkeypatch.setattr(app_module, 'HIGH_SCORES_FILENAME', str(temp_leaderboard_file))

    # Reset in-memory high scores list in the app module
    app_module.HIGH_SCORES = []
    
    # If a temp file somehow exists from a prior (failed) run, clear it
    if temp_leaderboard_file.exists():
        temp_leaderboard_file.unlink()
        
    # Call load_leaderboard to ensure app starts with a clean slate
    # (it will initialize HIGH_SCORES to [] if the temp file doesn't exist)
    app_module.load_leaderboard()

    yield # The test runs here

    # Teardown: Clean up in-memory state and file (though tmp_path handles file deletion)
    app_module.HIGH_SCORES = []
    if temp_leaderboard_file.exists():
        temp_leaderboard_file.unlink()

