import requests
from bs4 import BeautifulSoup
import re
NONCE = ""
GWTHeader =  "3B6C5196158464C5643BA376AF05E7F1"
GWTAUTH = "7|0|5|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|"
USERID = 0
def getANTICSRF(session):
    loginPageRequest = session.get("https://cronometer.com/login/")
    htmlLogin = loginPageRequest.text
    soup = BeautifulSoup(htmlLogin, 'html.parser')
    ANTICSRF = soup.find(type="hidden")['value']
    return ANTICSRF


def login(session, username, password):
    ANTICSRF = getANTICSRF(session)
    formData = {}
    formData["username"] = username
    formData["password"] = password
    formData["anticsrf"] = ANTICSRF
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    loginRequest = session.post("https://cronometer.com/login", data=formData, headers=headers)
    print(loginRequest)
    NONCE = loginRequest.cookies.get("sesnonce")
    gwtHeaders = {"content-type": "text/x-gwt-rpc; charset=UTF-8",
                  "x-gwt-module-base": "https://cronometer.com/cronometer/",
                  "x-gwt-permutation": "7B121DC5483BF272B1BC1916DA9FA963"}

    gwtRequest = session.post("https://cronometer.com/cronometer/app",headers=gwtHeaders,data=GWTAUTH)
    NONCE = gwtRequest.cookies.get("sesnonce")
    print(gwtRequest)
    USERID = re.findall("OK\[(?P<userid>\d*),.*",gwtRequest.text)[0]


session = requests.Session()

login(session, "username", "password")
