from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

#Global vars:
secret_number = 0
attempts_count = 0
MIN_NUMBER = 0
MAX_NUMBER = 1000
LEADERBOARD_FILE = 'leaderboard.json'
MAX_LEADERBOARD_ENTRIES = 5

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/new_game')
def new_game():
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_count = 0
    return jsonify({'message':f'New game has started! Guess a number between {MIN_NUMBER} and {MAX_NUMBER}'})

if __name__ == '__main__':
    app.run(debug=False)