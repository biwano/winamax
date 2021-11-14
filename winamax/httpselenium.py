import requests
import re
import json
import os
from seleniumwire import webdriver
from seleniumwire.utils import decode
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from . import db

os.environ['WDM_LOG_LEVEL'] = '0'

class Http():
    def __init__(self, suffix=""):
        self._data = None
        self.Session = db.Session()
        self.suffix = suffix

    def get_remote_data(self):
        res = {}
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        try:
            # Go to the Google home page
            driver.get(f"https://www.winamax.fr/paris-sportifs/sports{self.suffix}")
            p = re.compile(b'\["m",(\{.*\})\]')

            # Access requests via the `requests` attribute
            for request in driver.requests:
                if request.response and "EIO" in request.url:
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    m = p.search(body)
                    if m:
                        val = m.group(1)
                        try:
                            val = json.loads(val)
                        except Exception as e:
                            f = open("error.txt", "w")
                            f.write(val.decode('utf-8', errors='ignore'))
                            f.close()
                            raise(e)

                        if not val.get("matches"):
                            raise(Exception("Bad tournament type"))
                        res.update(val)
                        break
                        
                        
        except Exception as e:
            raise(e)
        finally:
            driver.quit()
        print(res)

        return res


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

