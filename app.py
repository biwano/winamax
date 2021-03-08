from flask import Flask, jsonify
from winamax import Winamax
app = Flask(__name__)

winamax = Winamax()

# sports
@app.route('/sports')
def get_sports():
    return jsonify(winamax.get_sports())

# matches
@app.route('/sports/<int:sport_id>/matches')
def get_matches(sport_id=None):
    return jsonify(winamax.get_matches(sport_id=sport_id))
