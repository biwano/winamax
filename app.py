from flask import Flask, Response
from winamax import Winamax
import json
app = Flask(__name__)

winamax = Winamax()

def jsonify(data):
	return Response(json.dumps(data, indent=2), mimetype='application/json')
# sports
@app.route('/sports')
def get_sports():
    return jsonify(winamax.get_sports())

# matches
@app.route('/sports/<int:sport_id>/matches')
def get_matches(sport_id=None):
    return jsonify(winamax.get_matches(sport_id=sport_id))

# match
@app.route('/matches/<int:match_id>')
def get_match(match_id=None):
    return jsonify(winamax.get_match(match_id=match_id))

# match history
@app.route('/matches/<int:match_id>/history')
def get_match_history(match_id=None):
    return jsonify(winamax.get_match_history(match_id=match_id))