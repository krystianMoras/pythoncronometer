from constants import *
import requests
import json
from bs4 import BeautifulSoup
import os.path
import re


# Cronometer client, handles all interactions between Cronometer server
class Client:
    def __init__(self, session):
        self.nonce = None
        self.userid = None
        self.session = session
        self.authtoken = None

    def _handleExceptions(self, request):
        if "EX" in request.text:
            if "Invalid or expired session" in request.text:
                print("Invalid or expired session")
                return False
            print(request.text)
            return False
        return True

    def _getANTICSRF(self):
        loginPageRequest = self.session.get(loginPageURL)
        htmlLogin = loginPageRequest.text
        soup = BeautifulSoup(htmlLogin, 'html.parser')
        ANTICSRF = soup.find(type="hidden")['value']
        return ANTICSRF

    def login(self, username, password):
        if not os.path.exists("cookies"):
            open("cookies", "w")
        cookie = open("cookies").read()
        if cookie != "":
            self.userid, self.nonce = cookie.split()
            print("Logged in")
            return True
        # to obtain anticsrf token, must "pretend" to be a website
        ANTICSRF = self._getANTICSRF()
        formData = {"username": username,
                    "password": password,
                    "anticsrf": ANTICSRF}
        loginRequest = self.session.post(loginRequestURL, data=formData, headers=regularHeaders)
        print(loginRequest)
        if "error" in loginRequest.text:
            error = json.loads(loginRequest.text)
            print(error["error"])
            return False
        self.nonce = loginRequest.cookies.get("sesnonce")
        # login to gwt API and get user id
        gwtRequest = self.session.post(GWTBaseURL, headers=gwtHeaders, data=GWTAUTH)

        self.nonce = gwtRequest.cookies.get("sesnonce")
        print(gwtRequest)
        if "EX" in gwtRequest.text:
            print(gwtRequest.text)
            return False
        self.userid = re.findall("OK\[(?P<userid>\d*),.*", gwtRequest.text)[0]
        cookieFile = open("cookies", "w")
        cookieFile.write(
            f"{self.userid} {self.nonce}")
        cookieFile.close()
        print("Logged in")
        return True

    # this token is required for every action
    def _getGWTToken(self):
        GWTGenerateAuthToken = GWTGenerateAuthFormat.format(nonce=self.nonce, userid=self.userid)
        request = self.session.post(GWTBaseURL, data=GWTGenerateAuthToken, headers=gwtHeaders)

        self.authtoken = re.findall("\"(?P<token>.*)\"", request.text)[0]
        print("gwt token found", self.authtoken)

    def exportDailyNutritionSummary(self, start, end):
        self._getGWTToken()
        print(self.authtoken)
        query = {"nonce": self.authtoken, "generate": "dailySummary", "start": start, "end": end}
        exportRequest = self.session.get(exportURL, params=query)
        # this one is different for some reason
        if exportRequest.status_code == 403:
            if "Invalid or expired session" in exportRequest.url:
                print("Invalid or expired session")
            return None
        print(exportRequest.text)
        return exportRequest.text




