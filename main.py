import requests
from dotenv import load_dotenv
import os
import time
import json
import Food
import re
from constants import nutrientIds
from CronometerClient import Client
load_dotenv()
USERNAME = os.environ.get("CRONOMETERUSERNAME")
PASSWORD = os.environ.get("CRONOMETERPASSWORD")

session = requests.Session()
client = Client(session)

client.login(USERNAME, PASSWORD)
client.getFood(455493)
client.logout()
client.getFood(455493)
client.login(USERNAME,PASSWORD)

