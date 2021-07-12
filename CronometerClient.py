from constants import *
import requests
from bs4 import BeautifulSoup
import re
class Client:
    def __init__(self,session):
        self.nonce = None
        self.userid = None
        self.session = session
        self.authtoken = None

    def _getANTICSRF(self):
        loginPageRequest = self.session.get(loginPageURL)
        htmlLogin = loginPageRequest.text
        soup = BeautifulSoup(htmlLogin, 'html.parser')
        ANTICSRF = soup.find(type="hidden")['value']
        return ANTICSRF

    def login(self, username, password):
        ANTICSRF = self._getANTICSRF()
        formData = {"username": username,
                    "password": password,
                    "anticsrf": ANTICSRF}
        loginRequest = self.session.post(loginRequestURL, data=formData, headers=regularHeaders)
        print(loginRequest)
        self.nonce = loginRequest.cookies.get("sesnonce")

        gwtRequest = self.session.post(GWTBaseURL, headers=gwtHeaders, data=GWTAUTH)
        self.nonce = gwtRequest.cookies.get("sesnonce")
        print(gwtRequest)
        self.userid = re.findall("OK\[(?P<userid>\d*),.*", gwtRequest.text)[0]

    def _getGWTToken(self):
        GWTGenerateAuthToken = GWTGenerateAuthFormat.format(nonce=self.nonce,userid=self.userid)
        request = self.session.post(GWTBaseURL, data=GWTGenerateAuthToken, headers=gwtHeaders)
        print(request)
        self.authtoken = re.findall("\"(?P<token>.*)\"", request.text)[0]


    def exportDailyNutrition(self, start, end):
        self._getGWTToken()
        query = {"nonce": self.authtoken, "generate": "dailySummary", "start": start, "end": end}
        exportRequest = self.session.get(exportURL, params=query)
        print(exportRequest)
        print(exportRequest.text)