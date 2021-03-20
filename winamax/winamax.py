import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db
from .http import Http
import time


class Winamax():
    def __init__(self):
        self._data = None
        self.Session = db.Session()

    def update_sports(self):
        http = Http()
        res_sports = []
        res_tournaments = []
        for sport_id in http.data["sports"]:
            sport = http.get("sports", sport_id)
            res_sport = { "name": sport["sportName"], "categories": []}
            for category_id in sport["categories"]:
                category = http.get("categories", category_id)
                res_category = {"name": category["categoryName"], "tournaments": []}
                res_sport["categories"].append(res_category)
                for tournament_id in category["tournaments"]:
                    tournament = http.get("tournaments", tournament_id)
                    res_tournament = {"name": tournament["tournamentName"],
                    "suffix": f"{sport_id}/{category_id}/{tournament_id}"}
                    res_category["tournaments"].append(res_tournament)
                    res_tournaments.append(res_tournament)
            res_sports.append(res_sport)
            

        db.update_config("sports", res_sports)
        db.update_config("tournaments", res_tournaments)

    def update_next_tournament(self):
        last_updated_tournament = db.get_config("last_updated_tournament")
        tournaments = db.get_config("tournaments")
        if last_updated_tournament == None:
            last_updated_tournament = -1
        else:
            last_updated_tournament = last_updated_tournament["value"]
        last_updated_tournament = last_updated_tournament + 1
        if last_updated_tournament >= len(tournaments):
            last_updated_tournament = 0
        suffix = tournaments[last_updated_tournament]["suffix"]
        print(suffix)
        self.update_tournament(suffix)
        db.update_config("last_updated_tournament", { "value": last_updated_tournament})
        


        
    def update_tournament(self, suffix):
        http = Http(suffix)
        for match_id in http.data["matches"]:
            match = http.data["matches"][match_id]
            bet = http.get("bets", match["mainBetId"])
            match["bet"] = bet
            db.update_match(match)
            for outcome_id in bet["outcomes"]:
                outcome = http.get("outcomes", outcome_id)
                outcome["outcomeId"] = outcome_id
                db.historize_outcome(outcome)



        
    """
    def update_sport_cache(self, cache, sport_id):
        cache = Cache(f"/{sport_id}")
        print(json.dumps(cache.data["categories"], indent=4))
        for category_id in cache.data["categories"]:
            break

    def update_cache(self, suffix):
        print(f"Updating cache {suffix}")
        local_cache = Cache(suffix)
        local_cache.update_cache()
        time.sleep(5)

    def update_all_caches(self):
        suffix = ""
        cache = Cache(suffix)
        for sport_id, sport in cache.data["sports"].items():
            self.update_cache(f"/{sport_id}")
            for category_id in sport["categories"]:
                category = cache.get_category(category_id)
                self.update_cache(f"/{sport_id}/{category_id}")
                for tournament_id in category["tournaments"]:
                    self.update_cache(f"/{sport_id}/{category_id}/{tournament_id}")
                    

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

    def clean_outcome_history(self):
        res = []
        with self.Session() as session:
            history = session.query(db.History.outcome_id).distinct()
            for outcome_id, in history:
                if not self.get_outcome(outcome_id):
                    session.query(db.History).filter_by(outcome_id=outcome_id).delete(synchronize_session=False)
                    res.append(outcome_id)
        return res            
            
    def serialize(self, history):
        return {
            "time": history.time,
            "data": json.loads(history.data),
        }

    def serialize_all(self, history):
        return [ self.serialize(h) for h in history ]
    """