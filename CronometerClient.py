from constants import *
import requests
import ResponseHandlers
import Food
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
        if "Invalid or expired session" in request.text:
            print("Invalid or expired session")
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
        cookieFile = open("cookies.txt", "w")
        cookieFile.write(f"{self.userid} {self.nonce}")
        cookieFile.close()
        print("Logged in")
        return True

    def logout(self):
        GWTLogout = GWTLogoutFormat.format(nonce=self.nonce)
        request = self.session.post(GWTBaseURL, data=GWTLogout, headers=gwtHeaders)
        if request.status_code == 200:
            print("Logged out", request.text)
        else:
            print("some error occured while trying to logout")
        cookieFile = open("cookies", "w")
        cookieFile.close()
        self.userid = None
        self.nonce = None

    # this token is required for every action
    def _getGWTToken(self):
        GWTGenerateAuthToken = GWTGenerateAuthFormat.format(nonce=self.nonce, userid=self.userid)
        request = self.session.post(GWTBaseURL, data=GWTGenerateAuthToken, headers=gwtHeaders)

        self.authtoken = re.findall("\"(?P<token>.*)\"", request.text)[0]
        print("gwt token found")

    def exportDailyNutritionSummary(self, start, end):
        self._getGWTToken()
        query = {"nonce": self.authtoken, "generate": "dailySummary", "start": start, "end": end}
        exportRequest = self.session.get(exportURL, params=query)
        # this one is different for some reason
        if exportRequest.status_code == 403:
            if "Invalid or expired session" in exportRequest.url:
                print("Invalid or expired session")
            return None
        print(exportRequest)
        return exportRequest.text

    def exportDailyServings(self, start, end):
        self._getGWTToken()
        query = {"nonce": self.authtoken, "generate": "servings", "start": start, "end": end}
        exportRequest = self.session.get(exportURL, params=query)
        # this one is different for some reason
        if exportRequest.status_code == 403:
            if "Invalid or expired session" in exportRequest.url:
                print("Invalid or expired session")
            return None
        print(exportRequest)
        return exportRequest.text

    def addServing(self, year, month, day, foodID, servingID, grams):
        GWTAddServing = GWTAddServingFormat.format(nonce=self.nonce, userid=self.userid, day=day, month=month,
                                                   year=year, foodID=foodID, servingID=servingID, grams=grams)
        request = self.session.post(GWTBaseURL, data=GWTAddServing, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None

        # this is alphabeticID of the serving, save it to edit/delete it later
        id = json.loads(request.text[4:])[0]
        print(f"Added {id}")
        return id

    def getFood(self, foodID):
        GWTGetFood = GWTGetFoodFormat.format(nonce=self.nonce, foodID=foodID)
        request = self.session.post(GWTBaseURL, data=GWTGetFood, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        jsonResponse = request.text[4:]
        array = json.loads(jsonResponse)
        food = Food.Food().jsonToFood(array)
        return food

    def findFood(self, query, number_of_suggestions=50):
        GWTFindFood = GWTFindFoodFormat.format(nonce=self.nonce, query=query,
                                               number_of_suggestions=number_of_suggestions)
        request = self.session.post(GWTBaseURL, data=GWTFindFood, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        jsonResponse = request.text

        return ResponseHandlers.extractFindFoodResponse(jsonResponse)

    def findMyFoods(self):
        GWTFindMyFoods = GWTFindMyFoodsFormat.format(nonce=self.nonce)
        request = self.session.post(GWTBaseURL, data=GWTFindMyFoods, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        jsonResponse = request.text
        return ResponseHandlers.extractCustomFoods(jsonResponse)

    def getDayInfo(self, year, month, day):
        GWTGetDayInfo = GWTGetDayInfoFormat.format(nonce=self.nonce, year=year, month=month, day=day,
                                                   userid=self.userid)
        request = self.session.post(GWTBaseURL, data=GWTGetDayInfo, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        jsonResponse = request.text[4:]
        return ResponseHandlers.extractDayInfoResponse(jsonResponse)

    def editServing(self, year, month, day, foodID, servingID, grams, alphabeticid):
        # uniqueid means sth but I set it to 0 and it still works
        GWTEditServing = GWTEditServingFormat.format(nonce=self.nonce, year=year, month=month, day=day,
                                                     userid=self.userid, alphabeticid=alphabeticid, servingid=servingID,
                                                     foodID=foodID, grams=grams, i=0, uniqueid=0)
        request = self.session.post(GWTBaseURL, data=GWTEditServing, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        print(f"Edited {alphabeticid}")
        print(request.text)

    def deleteServing(self, alphabeticid):
        GWTDeleteServing = GWTDeleteServingFormat.format(nonce=self.nonce, userid=self.userid,
                                                         alphabeticid=alphabeticid)
        request = self.session.post(GWTBaseURL, data=GWTDeleteServing, headers=gwtHeaders)
        if not self._handleExceptions(request):
            return None
        print(f"Deleted {alphabeticid}")
        print(request.text)
    # def addFood(self,name,food):
    #
    #     nutrientsString = food.convertToGWT()
    #     GWTAddFood = GWTAddFoodFormat.format(nonce=self.nonce, userid=self.userid,name=name,nutrientsString=nutrientsString)
    #     request = self.session.post(GWTBaseURL, data=GWTAddFood, headers=gwtHeaders)
    #     if not self._handleExceptions(request):
    #         return None
    #     print(request.text)
