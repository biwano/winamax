import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db
from .httpselenium import Http
from .http import Http as HttpStatic
from .browser import Browser
import time
from . import utils
from . import config
from datetime import datetime

def log(text):
    now = datetime.now() # current date and time
    date = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"[{date}] {text}")

class Winamax():
    def __init__(self):
        self._data = None
        self.Session = db.Session()
        self._sports = None

    @property
    def sports(self):
        if not self._sports:
            self._sports = db.get_config("sports")
        return self._sports
    

    def get_thing(self, thing_list, thing_id):
        if thing_list:
            for t in thing_list:
                if str(t.get("id")) == str(thing_id):
                    return t
        return {}

    def get_sport(self, sport_id):
        return self.get_thing(self.sports, sport_id)

    def get_category(self, sport_id, category_id):
        return self.get_thing(self.get_sport(sport_id).get("categories"), category_id)

    def get_tournament(self, sport_id, category_id, tournament_id):
        return self.get_thing(self.get_category(sport_id, category_id).get("tournaments"), tournament_id)

    def update_sports_nb_matches(self):
        for sport in self.sports:
            sport["matches"] = 0
            for category in sport["categories"]:
                category["matches"] = 0
                for tournament in category["tournaments"]:
                    db_matches = self.get_matches(tournament["id"])
                    tournament["matches"] = len(db_matches)
                    category["matches"] += tournament["matches"]
                sport["matches"] += category["matches"]
        db.update_config("sports", self.sports)

    def get_tournament_list(self):
        res_tournaments = []
        for sport in self.sports:
            for category in sport["categories"]:
                res_tournaments += category["tournaments"]
        return res_tournaments

    def update_tournament_config(self, sport_id, category_id, tournament_id, value):
        tournament = self.get_tournament(sport_id, category_id,tournament_id)
        tournament.update(value)
        db.update_config("sports", self.sports)
        return True




    def update_sports(self):
        http = HttpStatic()
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
                    # Get old tournament computed data
                    old_tournament = self.get_tournament(sport_id, category_id, tournament_id)
                    if old_tournament and "matches" in old_tournament:
                        res_tournament["matches"] = old_tournament["matches"]
                    else:
                        res_tournament["matches"] = 0

                    if old_tournament and "favorite" in old_tournament:
                        res_tournament["favorite"] = old_tournament["favorite"]
                    else:
                        res_tournament["favorite"] = False

                    res_category["tournaments"].append(res_tournament)
                    res_tournaments.append(res_tournament)

            res_sports.append(res_sport)

        db.update_config("sports", res_sports)
        db.update_config("tournaments", res_tournaments)
        self.update_sports_nb_matches()

    def suffix_explode(self, suffix):
        tmp = suffix.split("/")
        return (tmp[0], tmp[1], tmp[2])

    def update_next_tournament(self):
        last_updated_tournament = db.get_config("last_updated_tournament")
        tournaments = self.get_tournament_list()
        if last_updated_tournament == None:
            last_updated_tournament = -1
        else:
            last_updated_tournament = last_updated_tournament["value"]

        current_tournament = last_updated_tournament + 1
        while current_tournament != last_updated_tournament:
            if current_tournament >= len(tournaments):
                current_tournament = 0
            if True or tournaments[current_tournament].get("favorite"):
                suffix = tournaments[current_tournament]["suffix"]
                
                (sport_id, category_id, tournament_id) = self.suffix_explode(suffix)

                log(f"Rotating tournaments {current_tournament}/{len(tournaments)}")
                db.update_config("last_updated_tournament", { "value": current_tournament})
                http = Http(suffix)
                #self.update_tournament(Http(suffix), sport_id, category_id, tournament_id)
                self.update_tournament(HttpStatic(suffix), sport_id, category_id, tournament_id)
                return

            current_tournament += 1

        log("No favorite tournament")
            

        
    def update_tournament(self, http, sport_id, category_id, tournament_id):
        log(f"Updating tournament {sport_id}/{category_id}/{tournament_id}")
        suffix = f"/{sport_id}/{category_id}/{tournament_id}/"
        if not http.data.get("matches"):
            log(f"Bad data")
            return

        for match_id in http.data.get("matches"):
            match = http.data["matches"][match_id]
            bet = http.get("bets", match["mainBetId"])
            match["bet"] = bet
            db.update_match(match)
            if bet:
                for outcome_id in bet["outcomes"]:
                    outcome = http.get("outcomes", outcome_id)
                    if outcome:
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
        for match_id in http.data["matches"]:
            #if str(match["tournamentId"]) == str(tournament_id):
                if self.check_match(match_id):
                    self.send_match_notification(match_id=match_id)

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

    def check_outcome(self, outcome_id):
        log(f"Checking outcome {outcome_id}")
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
            log(f"- No data")
            return False
        first_odds = first.get("data").get("odds")
        last_odds = last.get("data").get("odds")
        if first_odds < 1 or first_odds > 2:
            log(f"- Bad odds: {first_odds}")
            return False

        diff = (first_odds - last_odds) / first_odds
        if abs(diff) < 0.05:
            log(f"- Weak variation: {diff}")
            return False            

        return True
    
    def matchInfo(self, match):
        res = ""
        def add(t):
            nonlocal res
            if res:
                res = res + "/"
            if t: 
                res = res + t["name"]
        add(self.get_sport(match['sportId']))
        add(self.get_category(match['sportId'], match['categoryId']))
        add(self.get_tournament(match['sportId'], match['categoryId'], match['tournamentId']))
        res = f'{res} - {match["competitor1Name"]} - {match["competitor2Name"]}'
        return res

    def check_match(self, match_id):
        match = self.get_match(match_id)
        match_start = match.get("matchStart")
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        log(f"Checking match {self.matchInfo(match)}")
        if not match.get('bet') or not match.get('bet').get('outcomes'):
            log(f" - no outcome")
            return False
        if match_start - timestamp < 60 * 10:
            log(f" - too late")
            return False
        if match_start - timestamp > 60 * 30:
            log(f" - too soon")
            return False
        for outcome_id in match.get('bet').get('outcomes'):
            if self.check_outcome(outcome_id):
                return True
        return False
    
    def test(self):
        http = Http("/1/44/207")
        http.get_remote_data()
