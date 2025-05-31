# Quick Draw Numbers - A Web Guessing Game

---
*Disclaimer: This project is being undertaken as a learning experience. AI (Google's Gemini) has been used to help brainstorm the project idea, outline the development plan, generate this README, and will be used as a general support tool throughout the development process.*
---

## Project Intent & Overview

**Quick Draw Numbers** is a simple web-based number guessing game designed as a Minimum Viable Product (MVP) to practice and demonstrate fundamental full-stack web development concepts. The game challenges players to guess a randomly generated number between 1 and 1000.

The primary goal is to build a functional application that includes:
* A frontend user interface (HTML, CSS, JavaScript) for player interaction.
* A backend API (Python with Flask) to manage game logic and data.
* Basic data persistence for a shared leaderboard using a JSON file.

This project serves as a hands-on exercise to understand client-server communication, API design, dynamic frontend updates, and basic backend development within a constrained timeframe (target: 10-15 hours of development).

## Core Features

* **New Game:** Players can start a new game, which generates a new secret random number (1-1000).
* **Guess Submission:** Players can submit their guesses via an input field.
* **Feedback:** The game provides feedback after each guess ("Too high!", "Too low!", or "Correct!").
* **Attempt Tracking:** The number of attempts for the current game is displayed.
* **Win Condition:** On correctly guessing the number, the player is notified.
* **Shared Leaderboard:**
    * Players who win can (optionally) submit their name and number of attempts to a shared leaderboard.
    * The leaderboard displays top scores (fewest attempts) across all games played.
    * Leaderboard data is stored in a simple JSON file on the server.

## Technology Stack

* **Frontend:**
    * HTML5
    * CSS3 (Basic styling, potentially with minimal Bootstrap for layout assistance)
    * Vanilla JavaScript (for DOM manipulation and API calls using the Fetch API)
* **Backend:**
    * Python 3.x
    * Flask (Micro web framework for serving the application and creating API endpoints)
* **Data Storage:**
    * **Current Game State:** In-memory variables on the Flask server (e.g., current secret number, attempts).
    * **Leaderboard:** A JSON file (`leaderboard.json`) on the server.
* **API:** Simple RESTful principles for frontend-backend communication.

## Development Plan Outline (Target: 10-15 hours)
Detailed summary of the plan is includeded in the developed [Training Package](https://github.com/MickWPM/number-guesser-fullstack/blob/main/Training%20Package.md)

The project will be developed in phases:

### Phase 1: Backend Foundation & Core Game Logic (Flask)
* **Objective:** Set up the Flask server and implement the core API endpoints for starting a new game and processing player guesses.
* **Key Tasks:**
    * Basic Flask application setup.
    * Implement `/api/new_game` endpoint (generates random number, resets attempts).
    * Implement `/api/guess` endpoint (compares guess, provides feedback, tracks attempts).
    * In-memory storage for the current secret number and attempts.

### Phase 2: Basic Frontend Structure & Interaction (HTML, JS)
* **Objective:** Create the user interface and implement JavaScript logic to interact with the core game APIs.
* **Key Tasks:**
    * Develop the basic HTML structure (`index.html`) for game display and player input.
    * Apply basic CSS for layout and styling.
    * Implement JavaScript to:
        * Call `/api/new_game` to initialize or reset the game.
        * Handle guess submissions.
        * Call `/api/guess` and dynamically update the UI with feedback and attempt counts.
        * Handle the win condition display.

### Phase 3: Leaderboard Implementation (Flask JSON & Frontend JS)
* **Objective:** Add the shared leaderboard functionality, including backend storage and frontend display/submission.
* **Key Tasks:**
    * **Backend:**
        * Implement helper functions in Flask to read from and write to `leaderboard.json`.
        * Create `GET /api/leaderboard` endpoint to retrieve leaderboard data.
        * Create `POST /api/leaderboard` endpoint to add new scores.
    * **Frontend:**
        * Implement JavaScript to fetch and display the leaderboard data.
        * Add UI elements for players to submit their name upon winning.
        * Implement JavaScript to send winning scores to `POST /api/leaderboard`.

### Phase 4: Polish & Testing
* **Objective:** Conduct thorough testing, fix bugs, and make minor usability improvements.
* **Key Tasks:**
    * Comprehensive gameplay testing, including edge cases.
    * Debugging any issues found in the frontend or backend.
    * Minor UI/UX refinements for clarity and ease of use.

### Future phases:
* Update github actions to automatically push updates to PythonAnywhere (or other hosted platform)
* Move high scores from local storage to database

## How to Run (Once Developed)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  **Install dependencies:**
    ```bash
    pip install Flask
    ```
3.  **Run the Flask application:**
    ```bash
    python app.py
    ```
4.  Open your web browser and navigate to `http://127.0.0.1:5000/`.

---
This README will be updated as the project progresses.
