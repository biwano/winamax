import requests
import re
import json
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

