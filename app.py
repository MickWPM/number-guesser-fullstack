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

if __name__ == '__main__':
    app.run(debug=False)