import requests
import re
import json
import os
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from seleniumwire.utils import decode
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from . import config

from . import db

os.environ['WDM_LOG_LEVEL'] = '0'

class Http():
    def __init__(self, suffix=""):
        self._data = None
        self.Session = db.Session()
        self.suffix = suffix
        self._driver = None

    @property
    def driver(self):
        if not self._driver:
            chrome_options = Options()
            chrome_options.add_argument("--window-size=800,600")
            chrome_options.add_experimental_option("detach", True)
            if config.selenium_headless:
                chrome_options.add_argument("--headless")

            self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            self._driver.implicitly_wait(10)

        return self._driver

    def get_remote_data(self):
        res = {}
        driver = self.get_driver()
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

                        #if not val.get("matches"):
                        #    print(json.dumps(val, indent=2))
                        #    raise(Exception("Bad tournament type"))
                        res.update(val)
        except Exception as e:
            raise(e)
        finally:
            driver.quit()

        return res

    def click(self, elem):
        self.driver.execute_script("arguments[0].click();",elem)


    def bet(self, match, outcome):
        print(json.dumps(match, indent=1))
        print(json.dumps(outcome, indent=1))
        match_id = match.get("matchId")
        self.driver.get("https://www.winamax.fr/account/login.php?redir=/")

        # cookie button
        cookie_button = self.driver.find_element(By.XPATH, "//button[@id='tarteaucitronPersonalize2']")
        sleep(1)
        self.click(cookie_button)

        # login iframe
        iframe = self.driver.find_element(By.XPATH, "//iframe[@id='iframe-login']")
        self.driver.switch_to.frame(iframe);
        
        # username 
        login = self.driver.find_element(By.XPATH, "//input[starts-with(@placeholder, 'Email')]")
        login.send_keys(config.winamax_login)

        # password
        password = self.driver.find_element(By.XPATH, "//input[starts-with(@placeholder, 'Mot de passe')]")
        password.send_keys(config.winamax_password)

        # login button
        submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.click(submit)

        # match page
        self.driver.get(f"https://www.winamax.fr/paris-sportifs/match/{match_id}")
        




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

