import requests
from CronometerClient import Client
import pandas
from io import StringIO
import yaml

with open('secrets.yaml') as f:
    secrets = yaml.load(f, Loader=yaml.FullLoader)
USERNAME = secrets['cronometer']['username']
PASSWORD = secrets['cronometer']['password']

session = requests.Session()
client = Client(session)
client.login(USERNAME, PASSWORD)
exported = StringIO(client.exportDailyNutritionSummary("2023-06-29", "2023-07-29"))
df = pandas.read_csv(exported)
print(df)