import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db
from .http import Http
from .browser import Browser
import time
from . import utils
from . import config


class Winamax():
    def __init__(self):
        self._data = None
        self.Session = db.Session()

    def get_thing(self, thing_list, thing_id):
        if thing_list:
            for t in thing_list:
                if t.get("id") == thing_id:
                    return t
        return {}

    def get_sport(self, sports, sport_id):
        return self.get_thing(sports, sport_id)

    def get_category(self, sports, sport_id, category_id):
        return self.get_thing(self.get_sport(sports, sport_id).get("categories"), category_id)

    def get_tournament(self, sports, sport_id, category_id, tournament_id):
        return self.get_thing(self.get_category(sports, sport_id, category_id).get("tournaments"), tournament_id)

    def update_sports_nb_matches(self,):
        sports = self.get_sports()
        for sport in sports:
            sport["matches"] = 0
            for category in sport["categories"]:
                category["matches"] = 0
                for tournament in category["tournaments"]:
                    db_matches = self.get_matches(tournament["id"])
                    tournament["matches"] = len(db_matches)
                    category["matches"] += tournament["matches"]
                sport["matches"] += category["matches"]
        db.update_config("sports", sports)

    def update_sports(self):
        http = Http()
        res_sports = []
        res_tournaments = []
        for sport_id in http.data["sports"]:
            sport = http.get("sports", sport_id)
            res_sport = { "id": sport_id, "name": sport["sportName"], "categories": []}
            for category_id in sport["categories"]:
                category = http.get("categories", category_id)
                res_category = {"id": category_id, "name": category["categoryName"], "tournaments": []}
                res_sport["categories"].append(res_category)
                for tournament_id in category["tournaments"]:
                    tournament = http.get("tournaments", tournament_id)
                    res_tournament = {"id": tournament_id, "name": tournament["tournamentName"],
                    "suffix": f"{sport_id}/{category_id}/{tournament_id}",
                    "sportId": sport_id,
                    "categoryId": category_id,
                    "tournamentId": tournament_id,
                    }
                    # Get old tournament compputed data
                    old_tournament = self.get_tournament(self.get_sports(), sport_id, category_id, tournament_id)
                    if old_tournament and "matches" in old_tournament:
                        res_tournament["matches"] = old_tournament["matches"]
                    else:
                        res_tournament["matches"] = 0
                    res_category["tournaments"].append(res_tournament)
                    res_tournaments.append(res_tournament)

            res_sports.append(res_sport)

        db.update_config("sports", res_sports)
        db.update_config("tournaments", res_tournaments)
        self.update_sports_nb_matches()

    def suffix_explode(self, suffix):
        tmp = suffix.split("/")
        return (tmp[0], tmp[1], tmp[2])

    def get_sports(self):
        return db.get_config("sports")

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
        
        (sport_id, category_id, tournament_id) = self.suffix_explode(suffix)
        self.update_tournament(sport_id, category_id, tournament_id)
        db.update_config("last_updated_tournament", { "value": last_updated_tournament})
        
        
    def update_tournament(self, sport_id, category_id, tournament_id):
        suffix = f"/{sport_id}/{category_id}/{tournament_id}/"
        http = Http(suffix)
        nb_matches = 0
        for match_id in http.data["matches"]:
            match = http.data["matches"][match_id]
            if match["tournamentId"] == tournament_id:
                nb_matches += 1
            bet = http.get("bets", match["mainBetId"])
            match["bet"] = bet
            db.update_match(match)
            if bet:
                for outcome_id in bet["outcomes"]:
                    outcome = http.get("outcomes", outcome_id)
                    outcome["outcomeId"] = outcome_id
                    outcome["odds"] = http.get("odds", outcome_id)
                    db.historize_outcome(outcome)

        # Delete expired matches and outcomes
        db_matches = self.get_matches(tournament_id)
        for match in db_matches:
            match_id = match["matchId"]
            if not http.exists("matches", match_id):
                bet = http.get("bets", match_id)
                if bet:
                    for outcome_id in bet["outcomes"]:
                        db.delete_outcome_history(outcome_id)
                db.delete_match(match_id)

        # update sports matches number
        self.update_sports_nb_matches()

        # Check matches for opportunities
        print(db_matches)
        for match_id in http.data["matches"]:
            if self.check_match(match_id):
                winamax.send_match_notification(match_id=match_id)


    def get_matches(self, tournament_id):
        with self.Session() as session:
             matches = session.query(db.Match).filter_by(tournament_id=tournament_id).all()
             return [ self.serialize_match(match) for match in matches ]

    def get_match(self, match_id):
        with self.Session() as session:
             match = session.query(db.Match).filter_by(match_id=match_id).one()
             return self.serialize_match(match)

    def serialize_match(self, match):
        return json.loads(match.value)

    def get_outcome(self, outcome_id):
        with self.Session() as session:
            history = session.query(db.History).filter_by(outcome_id=outcome_id).first()
            return self.serialize_history(history)["data"]

    def get_outcome_history(self, outcome_id):
        with self.Session() as session:
            histories = session.query(db.History).filter_by(outcome_id=outcome_id).order_by(db.History.time)

            return [ self.serialize_history(h) for h in histories.all() ]

    def serialize_history(self, history):
        return {
            "time": history.time,
            "data": json.loads(history.data),
        }

    def get_logs(self, nb_lines=50):
        logs = utils.get_last_n_lines('db.log', nb_lines)
        return logs

    def send_match_notification(self, match_id):
        match=self.get_match(match_id)
        subject = f"{match['competitor1Id'] - match['competitor2Id']}"
        message = f"""J'ai un tips pour toi<br/>
        Clique ici:<br/>
        <a href='{config.endpoint}/#/{match['sportId']}/{match['categoryId']}/{match['tournamentId']}/{match['matchId']}'
        """
        utils.send_mail(subject, message)
        return { "result": "ok"}

    def update_tournament_new(self, sport_id, category_id, tournament_id):
        suffix = f"/{sport_id}/{category_id}/{tournament_id}/"
        browser = Browser(suffix)
        browser.get_remote_data()

    def check_outcome(self, outcome_id):
        print(f"Checking outcome {outcome_id}")
        history = self.get_outcome_history(outcome_id)
        last = None
        first = None
        history.reverse()
        for dot in history:
            if not last:
                last = dot
            first = dot
            if last.get("time") - first.get("time") > 15 * 60:
                break
        if not first or not last:
            print(f"- No data")
            return False
        first_odds = first.get("data").get("odds")
        last_odds = last.get("data").get("odds")
        if first_odds < 1 or first_odds > 2:
            print(f"- Bad odds: {first_odds}")
            return False

        diff = (first_odds - last_odds) / first_odds
        if abs(diff) < 0.05:
            print(f"- Weak variation: {diff}")
            return False            

        return True
            
    def check_match(self, match_id):
        match = self.get_match(match_id)
        match_start = match.get("matchStart")
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        print(f"Checking match {match_id}")
        if not match.get('bet') or not match.get('bet').get('outcomes'):
            print(f" - no outcome")
            return False
        if match_start - timestamp < 60 * 10:
            print(f" - too late")
            return False
        if match_start - timestamp > 60 * 30:
            print(f" - too soon")
            return False
        for outcome_id in match.get('bet').get('outcomes'):
            if self.check_outcome(outcome_id):
                return True
        return False
            



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



    def clean_outcome_history(self):
        res = []
        with self.Session() as session:
            history = session.query(db.History.outcome_id).distinct()
            for outcome_id, in history:
                if not self.get_outcome(outcome_id):
                    session.query(db.History).filter_by(outcome_id=outcome_id).delete(synchronize_session=False)
                    res.append(outcome_id)
        return res            
           
    """                

