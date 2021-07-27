import requests
from dotenv import load_dotenv
import os
import Food
from CronometerClient import Client
load_dotenv()
USERNAME = os.environ.get("CRONOMETERUSERNAME")
PASSWORD = os.environ.get("CRONOMETERPASSWORD")

session = requests.Session()
client = Client(session)
client.login(USERNAME, PASSWORD)
food = Food.Food()
food.name = "Test Recipe"
#add 100 grams of Bananas in teaspoons
food.addIngredient(450856, 998947, 100)
food.id = client.addRecipe(food)




