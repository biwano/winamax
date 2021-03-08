import requests
import re
import json
import os
from http.cookiejar import LWPCookieJar
import copy

class Winamax():
    def __init__(self):
        self._data = None

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
        return sport

    def get_outcome(self, outcome_id):
        outcome = self.get_thing("outcomes", outcome_id)
        return outcome

    def get_bet(self, bet_id):
        bet = self.get_thing("bets", bet_id)
        if bet:
            outcomes = {}
            for i in range(len(bet["outcomes"])):
                outcome_id = bet["outcomes"][i]
                bet["outcomes"][i] = self.get_outcome(outcome_id)
                if bet["outcomes"][i]:
                    bet["outcomes"][i]["outcomeId"] = outcome_id
                    bet["outcomes"][i]["odds"] = self.get_thing("odds", outcome_id)

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
        sport_id=int(sport_id)
        for key, match in self.data["matches"].items():
            if not sport_id or sport_id == match["sportId"]:
                res.append(self.get_match(match["matchId"]))
        return res

    def get_sport(self, sport_id):
        sport = self.get_thing("sports", sport_id)
        if sport:
            sport["sportId"] = sport_id
            del sport["categories"]
            del sport["filters"]
            del sport["liveMatchCount"]
            del sport["mainMatchCount"]
            del sport["tvMatchCount"]
        return sport

    def get_sports(self):
        res = []
        for sport_id in self.data["sportIds"]:
            res.append(self.get_sport(sport_id))
        return res



