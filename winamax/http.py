import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db

class Http():
    def __init__(self, suffix=""):
        self._data = None
        self.Session = db.Session()
        self.suffix = suffix

    def extract(self, text):
        p= re.compile('var PRELOADED_STATE = (\{((?!\<script).)*});')
        m = p.search(text)
        if m:
            res = json.loads(m.group(1))
        else:
            print("Extraction failed: ")
            res = {}
        return res

    def get_remote_data(self):
        url = f"https://www.winamax.fr/paris-sportifs/sports{self.suffix}"
        response = requests.get(url)
        suffix = self.suffix.replace("/", ".")
        return self.extract(response.text)

    @property
    def data(self):
        if not self._data:
            self._data = self.get_remote_data()
        return self._data

    def exists(self, type, _id):
        _id = str(_id)
        return _id in self.data[type]

    def get(self, type, _id):
        _id = str(_id)
        if _id in self.data[type]:
            return self.data[type][_id]
        else:
            return None

    """
    @property
    def cache_file(self):
        suffix = self.suffix.replace("/", ".")
        return f"./cache/cache{suffix}.json"

    def get_cache(self):
        try:
            with open(self.cache_file, 'r') as infile:
                return json.load(infile)
        except:
            self.update_cache()
            return self.get_cache()

    def update_cache(self):
        data = self.get_remote_data()
        with open(self.cache_file, 'w') as outfile:
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

    def get_category(self, category_id):
        category = self.get_thing("categories", category_id)
        if category:
            category["categoryId"] = category_id
        return category

    def get_sport(self, sport_id):
        sport = self.get_thing("sports", sport_id)
        if sport and "categories" in sport:
            sport["sportId"] = sport_id
            del sport["categories"]
            del sport["filters"]
        return sport

    def get_outcome(self, outcome_id):
        outcome = self.get_thing("outcomes", outcome_id)
        if outcome:
            outcome["outcomeId"] = outcome_id
        return outcome

    def get_bet(self, bet_id):
        bet = self.get_thing("bets", bet_id)

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
        for outcome_id, outcome in self.data["outcomes"].items():
            outcome = self.get_outcome(outcome_id)
            if outcome:
                outcome["odds"] = self.get_thing("odds", outcome_id)
                res.append(outcome)
        return res
    """