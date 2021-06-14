import requests
import re
import json
import os
from datetime import datetime
from http.cookiejar import LWPCookieJar
import copy
from . import db

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import hashlib


        

class Browser():
    def __init__(self, suffix=""):
        self._data = None
        self.Session = db.Session()
        self.suffix = suffix

    def get_elem(self, elem, sequence):
        if len(sequence)>0:
            i = sequence.pop(0)
            childs = elem.find_elements_by_xpath("./child::*")
            if i < len(childs):
                return self.get_elem(childs[i], sequence)
        else:
            return elem

    def get_text(self, elem, sequence):
        elem = self.get_elem(elem, sequence)
        if elem:
            return elem.text

    def hash(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()


    def get_remote_data(self):
        driver = webdriver.Firefox()
        driver.get(f'https://www.winamax.fr')
        wait = WebDriverWait(driver, 10)

        elem = driver.find_element_by_xpath('//a[@href="/paris-sportifs"]')
        elem.click()
        driver.get(f'https://www.winamax.fr/paris-sportifs/sports/{self.suffix}')
        xpath = '//a[contains(@href, "/paris-sportifs/match/")]'
        men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
        elems = driver.find_elements_by_xpath(xpath)
        matches = []
        for elem in elems:
            opps = self.get_text(elem, [0, 0, 0])
            if opps and " - " in opps:
                opponents = opps.split(" - ")
                print(opps, opponents)
                outcomes = []
                
                for i in range(3):
                    elem_i = self.get_elem(elem, [0, 1, 0, i])
                    odds = self.get_text(elem_i, [0, 0, 0])
                    if odds:
                        code = self.get_text(elem_i, [0, 0, 3, 0])
                        percentDistribution = self.get_text(elem_i, [0, 1, 0])
                        outcome_id = self.hash(f"{opps}_{code}")
                        if code=="N":
                            label = "Match nul"
                        else:
                            label = opponents[int(code) - 1]
                        outcomes.append({
                            "outcomeId": outcome_id,
                            "code": code,
                            "percentDistribution": percentDistribution,
                            "odds": odds,
                            "label": label
                            })
                match_id = self.hash(opps)
                match = {
                    "matchId": match_id,
                    "competitor1Name": opponents[0],
                    "competitor2Name": opponents[1],
                    "outcomes": outcomes
                }
                matches.append(match)
        print(json.dumps(matches, indent=2))


                    

   

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