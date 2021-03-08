import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db

class Winamax():
    def __init__(self):
        self._data = None
        self.Session = db.Session()

    def extract(self, text):
        p= re.compile('var PRELOADED_STATE = (\{((?!\<script).)*});')
        m = p.search(text)
        res = json.loads(m.group(1))
        return res

    def get_remote_data(self):
        url = f"https://www.winamax.fr/paris-sportifs/sports/"
        response = requests.get(url)
        return self.extract(response.text)

    def get_cache(self):
        try:
            with open(f'./cache.json', 'r') as infile:
                return json.load(infile)
        except:
            self.update_cache()
            return self.get_cache()

    def update_cache(self):
        data = self.get_remote_data()
        with open(f'./cache.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
            self._data = None

    @property
    def data(self):
        if not self._data:
            self._data = self.get_cache()
        return self._data


    def get_thing(self, type, type_id):
        type_id = str(type_id)
        thing = self.data[f"{type}"].get(type_id)
        return copy.deepcopy(thing)

    def get_sport(self, sport_id):
        sport = self.get_thing("sports", sport_id)
        if sport and "categories" in sport:
            del sport["categories"]
            del sport["filters"]
            del sport["liveMatchCount"]
            del sport["mainMatchCount"]
            del sport["tvMatchCount"]
        return sport

    def get_outcome(self, outcome_id):
        outcome = self.get_thing("outcomes", outcome_id)
        outcome["outcomeId"] = outcome_id
        return outcome

    def get_bet(self, bet_id):
        bet = self.get_thing("bets", bet_id)
        """
        if bet:
            outcomes = {}
            for i in range(len(bet["outcomes"])):
                outcome_id = bet["outcomes"][i]
                bet["outcomes"][i] = self.get_outcome(outcome_id)
                if bet["outcomes"][i]:
                    bet["outcomes"][i]["outcomeId"] = outcome_id
                    bet["outcomes"][i]["odds"] = self.get_thing("odds", outcome_id)
        """

        return bet


    def get_match(self, match_id):
        match = self.get_thing("matches", match_id)
        if match:
            match["bet"] = self.get_bet(match["mainBetId"])
            match["sport"] = self.get_sport(match["sportId"])
            del match["filters"]
        return match

    def get_matches(self, sport_id=None):
        res = []
        for key, match in self.data["matches"].items():
            if not sport_id or sport_id == match["sportId"]:
                res.append(self.get_match(match["matchId"]))
        return res


    def get_sports(self):
        res = []
        for sport_id in self.data["sportIds"]:
            res.append(self.get_sport(sport_id))
        return res

    def get_outcomes(self):
        res = []
        print(self.data["outcomes"])
        for outcome_id, outcome in self.data["outcomes"].items():
            res.append(self.get_outcome(outcome_id))
        return res


    def take_outcomes_snapshot(self):
        self.update_cache()
        time = datetime.now().timestamp()
        with self.Session() as session:
            for outcome in self.get_outcomes():
                history = db.History(
                outcome_id=outcome["outcomeId"],
                time=time,
                data=json.dumps(outcome))
                session.add(history)

    def get_outcome_history(self, outcome_id):
        with self.Session() as session:
            history = session.query(db.History).filter_by(outcome_id=outcome_id)
            return self.serialize_all(history.all())
            
    def serialize(self, history):
        return {
            "time": history.time,
            "data": json.loads(history.data),
        }

    def serialize_all(self, history):
        return [ self.serialize(h) for h in history ]
