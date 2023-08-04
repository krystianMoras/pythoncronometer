# pythoncronometer
Export nutrition data from cronometer
rewritten from https://github.com/jrmycanady/gocronometer
# Usage

Start a client
```python
import requests
import Food
from CronometerClient import Client

session = requests.Session()
client = Client(session)
```
Login to the cronometer
```python
client.login("username","password")
```

You can also export daily summary and servings
```python
import pandas
exported = StringIO(client.exportDailyNutritionSummary("2023-06-29", "2023-07-29"))
df = pandas.read_csv(exported)
print(df)
```
Logout
```python
client.logout()
```
Note: login() saves your userID and nonce to the cookies file and reuses it if it's not empty, so you don't have to logout() every time
