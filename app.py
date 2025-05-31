from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

#Global vars:
secret_number = 0
attempts_count = 0
game_over = False
MIN_NUMBER = 0
MAX_NUMBER = 10
LEADERBOARD_FILE = 'leaderboard.json'
MAX_LEADERBOARD_ENTRIES = 5
NEW_GAME_MESSAGE = f'New game has started! Guess a number between {MIN_NUMBER} and {MAX_NUMBER}'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/new_game')
def new_game():
    global attempts_count, game_over, secret_number
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_count = 0
    game_over = False
    print(f'Secret number generated as {secret_number}')
    return jsonify({'message':NEW_GAME_MESSAGE})

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
        feedback = 'Too high! :('
    else:
        feedback = 'Too low! :('
    
    return jsonify({
        'feedback': feedback,
        'attempts_count': attempts_count,
        'game_over': game_over
    })


if __name__ == '__main__':
    app.run(debug=False)