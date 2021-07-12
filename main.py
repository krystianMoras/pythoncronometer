import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
from constants import *
from CronometerClient import Client
load_dotenv()
USERNAME = os.environ.get("CRONOMETERUSERNAME")
PASSWORD = os.environ.get("CRONOMETERPASSWORD")

session = requests.Session()
client = Client(session)
client.login(USERNAME, PASSWORD)
client.exportDailyNutrition("2019-01-01", "2021-07-11")
