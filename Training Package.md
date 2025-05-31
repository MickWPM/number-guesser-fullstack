# Training Package: "Quick Draw Numbers" MVP (10-15 Hours)

## 1. Project Recap:

* **Name:** Quick Draw Numbers
* **Goal:** Build a web-based number guessing game where players guess a number between 1 and 1000. The backend (Python/Flask) provides an API for game logic and a shared leaderboard. The frontend (HTML, CSS, JavaScript) allows interaction.
* **Core Features:** New game, guess submission, high/low/correct feedback, attempts tracking, optional name submission to a shared JSON-based leaderboard.
* **Tech Stack:**
    * **Frontend:** HTML, Basic CSS (or minimal Bootstrap), Vanilla JavaScript (Fetch API)
    * **Backend:** Python, Flask
    * **Storage:** In-memory for current game state (secret number, attempts), JSON file for leaderboard.
* **Target Time:** 10-15 hours

## 2. Prerequisites & Setup:

* **Python 3:** Ensure Python 3 is installed on your system.
* **Text Editor:** A good text editor or IDE (e.g., VS Code, Sublime Text, PyCharm Community).
* **Web Browser:** For testing (Chrome, Firefox, Edge).
* **Flask Installation:** Open your terminal or command prompt and run: `pip install Flask`
* **Project Folder:** Create a main folder for your project (e.g., `quick_draw_game`). Inside it, create:
    * `app.py` (for your Flask backend code)
    * A `templates` folder (for `index.html`)
    * A `static` folder (for `style.css` and `script.js`)

## 3. Overall Time Management:

This plan is broken into phases. Try to stick to the estimated times, but they are flexible. If you finish a section early, move on. If you get stuck, don't spend too long – simplify or make a note to revisit if time allows. **Test frequently!**

---

## Phase 1: Backend Foundation & Core Game Logic (Flask) (Est. 3 - 4 hours)

* **Objective:** Create the Flask server, API endpoints for starting a game, and making a guess. The secret number will be stored in memory.

* **Tasks:**
    1.  **Basic Flask App Setup (0.5 - 1 hour)**
        * In `app.py`, import `Flask`, `jsonify`, `request` from `flask` and `random`.
        * Initialize your Flask app: `app = Flask(__name__)`.
        * Create a global variable (or variables within your app context) to store `secret_number` and `attempts_count`. Initialize them (e.g., `secret_number = 0`, `attempts_count = 0`).
        * Define `LEADERBOARD_FILE = 'leaderboard.json'`.
        * Create a basic route `@app.route('/')` that serves your `index.html` file.
            ```python
            from flask import Flask, render_template, jsonify, request
            import random
            import json # Import for leaderboard
            import os # Import for checking if leaderboard file exists

            app = Flask(__name__)

            # Global variables for game state
            secret_number = 0
            attempts_count = 0
            LEADERBOARD_FILE = 'leaderboard.json'
            MAX_LEADERBOARD_ENTRIES = 5 # Optional: Limit leaderboard size

            @app.route('/')
            def home():
                return render_template('index.html')

            # ... (API endpoints will be added here) ...

            if __name__ == '__main__':
                app.run(debug=True)
            ```
        * **Test:** Run `python app.py`. Visiting `http://127.0.0.1:5000/` will error until `index.html` is created.

    2.  **`/api/new_game` Endpoint (1 - 1.5 hours)**
        * Define this route in `app.py`.
        * Generate a new random integer (1-1000) for `secret_number`.
        * Reset `attempts_count` to 0.
        * Return a JSON response, e.g., `jsonify({'message': 'New game started! Guess a number between 1 and 1000.'})`.
        * **Test:** Use your browser or Postman/Insomnia for `http://127.0.0.1:5000/api/new_game`.

    3.  **`/api/guess` Endpoint (1.5 - 2 hours)**
        * Define this `POST` route in `app.py`.
        * Get `player_guess` from incoming JSON: `data = request.get_json()`, `player_guess = data.get('guess')`.
        * **Basic Input Validation:** Check if `player_guess` is an integer.
        * Increment `attempts_count`.
        * Compare `player_guess` with `secret_number` (feedback: "low", "high", "correct").
        * Determine `game_over` status.
        * Return JSON: `jsonify({'feedback': feedback, 'attempts': attempts_count, 'game_over': game_over})`.
        * **Test:** Use Postman/Insomnia to `POST` guesses.

* **Key Learning:** Flask routing, request handling (JSON), JSON responses, basic Python logic.

---

## Phase 2: Basic Frontend Structure & Interaction (HTML, JS) (Est. 3 - 4.5 hours)

* **Objective:** Create the HTML page and write JavaScript to call the backend APIs and update the page dynamically.

* **Tasks:**
    1.  **HTML Structure (`templates/index.html`) (1 - 1.5 hours)**
        * Create `index.html` in `templates`.
        * Basic HTML boilerplate.
        * `<head>`: Title, link to `style.css` (`{{ url_for('static', filename='style.css') }}`).
        * `<body>`: Layout sections (Header, Game Status & Feedback, Player Input, Game Control, Win State, Leaderboard) with `id` attributes for JS interaction.
        * Link `script.js` at the *bottom* of `<body>` (`{{ url_for('static', filename='script.js') }}`).
        * **Test:** Refresh `http://127.0.0.1:5000/`. See basic HTML.

    2.  **Basic CSS (`static/style.css`) (0.5 hours)**
        * Create `style.css` in `static`.
        * Add minimal CSS for basic layout (centering, margins, etc.).
        * Style `#win-section` with `display: none;` initially.

    3.  **JavaScript - Game Initialization & New Game (`static/script.js`) (0.5 - 1 hour)**
        * Create `script.js` in `static`.
        * Get DOM element references.
        * `startNewGame()` function:
            * `fetch('/api/new_game')`.
            * Update feedback message, reset attempts on page to 0.
            * Clear guess input, hide win section, show guess section.
        * Event listener for "New Game" button to call `startNewGame()`.
        * Call `startNewGame()` on page load.
        * **Test:** Load page. New game starts. "New Game" button works.

    4.  **JavaScript - Guess Submission & Feedback (1 - 1.5 hours)**
        * `submitGuess()` function (or handle in event listener for "Submit Guess" button).
        * Get guess value, convert to number. Basic frontend validation.
        * `fetch('/api/guess', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({guess: guessValue}) })`.
        * Process response: update feedback message, attempts counter.
        * If correct: show "Win State" section, display final attempts, (optional) disable guess input.
        * Clear guess input.
        * **Test:** Play the game! Check feedback, attempts, win condition.

* **Key Learning:** HTML structure, basic CSS, DOM manipulation, `fetch` API (GET/POST), JSON handling in JS, event listeners.

---

## Phase 3: Leaderboard Implementation (Est. 3 - 4 hours)

* **Objective:** Implement backend logic for JSON leaderboard storage and frontend display/submission.

* **Tasks:**
    1.  **Backend - Leaderboard File Handling & `/api/leaderboard` GET (Flask) (1 - 1.5 hours)**
        * In `app.py`:
            * `load_leaderboard()`: Reads `LEADERBOARD_FILE`. Handles file not found (return empty list) and JSON errors.
            * `save_leaderboard(scores)`: Writes scores to `LEADERBOARD_FILE`.
        * Implement `GET /api/leaderboard` endpoint: calls `load_leaderboard()`, returns scores as JSON.
        * **Test:** Manually create `leaderboard.json` with dummy data. Hit `/api/leaderboard` via browser/Postman.

    2.  **Backend - `/api/leaderboard` POST (Flask) (0.5 - 1 hour)**
        * Implement `POST /api/leaderboard` endpoint:
            * Get `name` and `attempts` from request JSON.
            * `scores = load_leaderboard()`.
            * Add new score: `new_score = {"name": name, "attempts": int(attempts)}`.
            * Append to `scores`. Sort by attempts (ascending).
            * (Optional) Trim to `MAX_LEADERBOARD_ENTRIES`.
            * `save_leaderboard(scores)`.
            * Return success JSON.
        * **Test:** Use Postman to `POST` scores. Check `leaderboard.json` updates.

    3.  **Frontend - Display Leaderboard (JavaScript) (0.5 - 1 hour)**
        * In `script.js`, `fetchAndDisplayLeaderboard()` function:
            * `fetch('/api/leaderboard')`.
            * Clear current leaderboard display (`id="leaderboard-list"`).
            * Iterate scores, create `<li>` elements, append to display.
            * Handle "No scores yet" message.
        * Call on page load and after successful score submission.
        * **Test:** Refresh page. Leaderboard displays.

    4.  **Frontend - Submit Score to Leaderboard (JavaScript) (0.5 - 1 hour)**
        * In `script.js`, event listener for "Add to Leaderboard" button (`id="submit-score-button"`).
        * Get player name and win attempts (store attempts in a JS variable upon winning).
        * Basic frontend validation (name not empty).
        * `POST` name and attempts to `/api/leaderboard`.
        * On success: call `fetchAndDisplayLeaderboard()`, hide win section (or just name input/submit part), show "Score submitted!" message.
        * **Test:** Win game, submit score. Check leaderboard updates on page and in `leaderboard.json`.

* **Key Learning:** File I/O in Python (JSON), data structuring, complex frontend-backend interaction, dynamic list generation.

---

## Phase 4: Polish & Testing (Est. 1 - 1.5 hours)

* **Objective:** Final testing, bug fixing, and minor improvements.

* **Tasks:**
    1.  **Comprehensive Testing (0.5 - 1 hour)**
        * Play multiple times. Test edge cases (non-numeric guess, empty name).
        * Check browser and Flask consoles for errors.
        * Verify `leaderboard.json` behavior (creation, updates, sorting).

    2.  **Minor UI/UX Tweaks (0.5 hours)**
        * Adjust CSS for clarity/spacing.
        * Ensure feedback messages are user-friendly.
        * Refine game flow (e.g., what happens after score submission).

* **Key Learning:** Debugging, importance of testing, user experience considerations.

---

## Tips for Success in 10-15 Hours:

* **KISS (Keep It Super Simple):** If behind, cut non-essential flair. Core game loop and API are key.
* **Test Iteratively:** Test after almost every small task. Use `print()` and `console.log()`.
* **Focus:** One thing at a time.
* **Read Errors Carefully.**
* **Perfection is the Enemy of Good:** Aim for *working*, not perfect.
* **Use Online Resources:** MDN, Flask docs, Stack Overflow for specific issues.
