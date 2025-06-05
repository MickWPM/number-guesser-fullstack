from flask import Flask, render_template, jsonify, request
import random, os, json

app = Flask(__name__)

#Global vars:
secret_number = 0
attempts_count = 0
game_over = False
MIN_NUMBER = 1
MAX_NUMBER = 1000
LEADERBOARD_FILE = 'leaderboard.json'
MAX_LEADERBOARD_ENTRIES = 5
NEW_GAME_MESSAGE = f'New game has started! Guess a number between {MIN_NUMBER} and {MAX_NUMBER}'
GUESS_LOW_MESSAGE = 'Too low! :('
GUESS_HIGH_MESSAGE = 'Too high! :('
MAX_SCORES_TO_KEEP=10
MAX_SCORES_TO_SHOW=5
HIGH_SCORES = []
HIGH_SCORES_FILENAME = "high_scores.json"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/game_info')
def get_game_info():
    return jsonify({
        'min_num': MIN_NUMBER,
        'max_num': MAX_NUMBER,
        'game_description': 'Probably the greatest guessing game of all. Guess a number, be told too high or too low.... keep going till you get it!'
    })

@app.route('/api/new_game')
def new_game():
    global attempts_count, game_over, secret_number
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_count = 0
    game_over = False
    print(f'Secret number generated as {secret_number}')
    return jsonify({'message':NEW_GAME_MESSAGE})

@app.route('/api/leaderboard', methods=['POST'])
def add_high_score():
    data = request.get_json()
    player_name = data.get('name')
    player_score = data.get('score')
    add_score_to_leaderboard(player_name, player_score)
    return jsonify({'success':True})


@app.route('/api/leaderboard', methods=['GET'])
def get_high_scores():
    global HIGH_SCORES, MAX_SCORES_TO_SHOW
    return jsonify(HIGH_SCORES[:MAX_SCORES_TO_SHOW])

def load_leaderboard():
    global HIGH_SCORES_FILENAME, HIGH_SCORES, MAX_SCORES_TO_KEEP
    
    if(os.path.exists(HIGH_SCORES_FILENAME)):
        try:
            with open(HIGH_SCORES_FILENAME, 'r') as f:
                data = json.load(f)
                # Optional: Add some validation to ensure data is a list of dicts
                # For now, we'll assume the format is correct if the file loads
                if isinstance(data, list):
                    HIGH_SCORES = data
                    print(f"Leaderboard loaded successfully from {HIGH_SCORES_FILENAME}.")
                else:
                    print(f"Warning: {HIGH_SCORES_FILENAME} does not contain a valid list. Initializing empty leaderboard.")
                    HIGH_SCORES = [] # Fallback if JSON is not a list
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {HIGH_SCORES_FILENAME}. File might be corrupted. Initializing empty leaderboard.")
            HIGH_SCORES = [] # Initialize to empty if JSON is invalid
        except IOError:
            print(f"Error: Could not read file {HIGH_SCORES_FILENAME}. Initializing empty leaderboard.")
            HIGH_SCORES = [] # Initialize to empty if file can't be read
        except Exception as e:
            print(f"An unexpected error occurred while loading {HIGH_SCORES_FILENAME}: {e}. Initializing empty leaderboard.")
            HIGH_SCORES = []
    else:
        print(f"{HIGH_SCORES_FILENAME} not found. Initializing a new empty leaderboard.")
        HIGH_SCORES = [] # Ensure it's explicitly empty if file doesn't exist

def save_leaderboard():
    global HIGH_SCORES, MAX_SCORES_TO_KEEP # We might update HIGH_SCORES if we are saving to it

    if MAX_SCORES_TO_KEEP is not None:
        # Sort by score (lower is better) and then take MAX_SCORES_TO_KEEP
        # Ensure items are dictionaries and have a 'score' key
        try:
            processed_scores = sorted(
                [s for s in HIGH_SCORES if isinstance(s, dict) and 'score' in s],
                key=lambda item: item['score']
            )[:MAX_SCORES_TO_KEEP]
        except TypeError:
            print("Error: Scores list contains items not suitable for sorting or missing 'score' key.")
            return # Don't save if data is malformed
    else:
        processed_scores = HIGH_SCORES

    try:
        with open(HIGH_SCORES_FILENAME, 'w') as f:
            json.dump(processed_scores, f, indent=4)
        print(f"Leaderboard saved successfully to {HIGH_SCORES_FILENAME} with {len(processed_scores)} entries.")
        HIGH_SCORES = processed_scores # Update global list with what was saved
    except IOError:
        print(f"Error: Could not write to file {HIGH_SCORES_FILENAME}.")
    except Exception as e:
        print(f"An unexpected error occurred while saving {HIGH_SCORES_FILENAME}: {e}.")


def add_score_to_leaderboard(name, score):
    """
    Adds a new score to the global HIGH_SCORES, keeps it sorted (lower is better),
    and trims it to max_entries.
    Args:
        name (str): Player's name.
        score (int): Player's score.
        max_entries (int): Maximum number of entries to keep in the leaderboard.
    """
    global HIGH_SCORES, MAX_SCORES_TO_KEEP
    HIGH_SCORES.append({"name": name, "score": score})
    # Sort by score (lower is better)
    HIGH_SCORES.sort(key=lambda item: item['score'])
    # Keep only the top 'max_entries' scores
    HIGH_SCORES = HIGH_SCORES[:MAX_SCORES_TO_KEEP]
    print(f"Score for {name} ({score}) added. Leaderboard has {len(HIGH_SCORES)} entries.")
    save_leaderboard()




@app.route('/api/guess', methods=['POST'])
def guess_number():
    global attempts_count, game_over
    if game_over:
        return jsonify({
        'feedback': f'You have already won this game! You guessed the number was {secret_number} in {attempts_count} guesses',
        'attempts_count': attempts_count,
        'game_over': game_over
        })
    data = request.get_json()
    player_guess = data.get('guess')

    if not data or 'guess' not in data:
        return jsonify({'error': 'Missing guess in request body'}), 400 

    if not isinstance(player_guess, int):
        return jsonify({'error': 'Guess must be an integer.'}), 400
    
    attempts_count += 1

    feedback = ''
    if player_guess == secret_number:
        feedback = f'You guessed it in {attempts_count}!'
        game_over = True
    elif player_guess > secret_number:
        feedback = GUESS_HIGH_MESSAGE
    else:
        feedback = GUESS_LOW_MESSAGE
    
    return jsonify({
        'feedback': feedback,
        'attempts_count': attempts_count,
        'game_over': game_over
    })


if __name__ == '__main__':
    load_leaderboard()
    app.run(debug=False)