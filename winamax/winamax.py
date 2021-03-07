import requests
import re
import json
import os
from http.cookiejar import LWPCookieJar

class Winamax():
	def __init__(self):
		self._data = None


	@property
	def data(self):
		if not self._data:
			url = f"https://www.winamax.fr/paris-sportifs/sports/"
			response = self.session.get(url)
			self._data = self.extract(response.text)
		return self._data

	def extract(self, text):
		p= re.compile('var PRELOADED_STATE = (\{((?!\<script).)*});')
		m = p.search(text)
		res = json.loads(m.group(1))
		return res

	def get_thing(self, type, type_id):
		type_id = str(type_id)
		thing = self.data[f"{type}"].get(type_id)
		return thing

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

	def get_matches(self):
		res = []
		for key, match in self.data["matches"].items():
			res.append(self.get_match(match["matchId"]))
		return res


	def post(self, param="", data=None):
		url = f"https://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/?language=FR&version=1.80.3&EIO=3&transport=polling&t=NWDcAga{param}"
		print(url)

		response = self.session.post(url,
			data=data)
		return response

