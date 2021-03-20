from flask import Flask, Response
from flask_cors import CORS
from winamax import Winamax
import json

app = Flask(__name__)
cors = CORS(app)

winamax = Winamax()

def jsonify(data):
	return Response(json.dumps(data, indent=2), mimetype='application/json')
# sports
@app.route('/sports')
def get_sports():
    return jsonify(winamax.get_sports())

# matches
@app.route('/tournaments/<int:tournament_id>/matches')
def get_matches(tournament_id):
    return jsonify(winamax.get_matches(tournament_id=tournament_id))

# match
@app.route('/matches/<int:match_id>')
def get_match(match_id=None):
    return jsonify(winamax.get_match(match_id=match_id))

# outcome
@app.route('/outcomes/<int:outcome_id>')
def get_outcome(outcome_id=None):
	return jsonify(winamax.get_outcome(outcome_id=outcome_id))

# outcome history
@app.route('/outcomes/<int:outcome_id>/history')
def get_outcome_history(outcome_id=None):
    return jsonify(winamax.get_outcome_history(outcome_id=outcome_id))