# pythoncronometer
Since Cronometer won't release API this python library allows to communicate with Cronometer without going through their site.

If Cronometer team does not want this to be public feel free to contact me.
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
Add meal to diary
e.g. add 1000 ml of tap water on 6th July 2021
```python
#client.addServing(year,month,day,foodID,servingID,grams)
alphabeticid = client.addServing(2021,7,6,455493,9942233,1000)
```
Edit
```python
client.editServing(2021,7,26,455493,9942233,10,alphabeticid)
```
Delete
```python
client.deleteServing(alphabeticid)
```
To obtain serving ID and food ID you can use following methods
```python
print(client.findFood("tap water",5))
#{'Tea, Black, Brewed, Prepared with Tap Water': 7027, 'Beverages, Water, Tap, Municipal': 6646, 'Beverages, Water, Tap, Drinking': 6643, 'Beverages, Water, Tap, Well': 6640, 'Tap Water': 455493}
print(client.getFood(455493).servingsList[0])
#ServingId=9942233 Name="mL" Weight=1.0g
```
Create custom recipes
```python
food = Food.Food()
food.name = "Test Recipe"
#add 100 grams of Bananas in teaspoons
food.addIngredient(450856, 998947, 100)
food.id = client.addRecipe(food)
```
Edit recipes
```python
#add 10 ml of water
food.addIngredient(455493,9942233,10)
client.editRecipe(food)
```
Get all custom foods names and ids
```python
print(client.findMyFoods())
```
You can also export daily summary and servings
```python
import pandas
exported = StringIO(client.exportDailyServings("2021-07-13","2021-07-13"))
df = pandas.read_csv(exported)
print(df)
```
Logout
```python
client.logout()
```
Note: login() saves your userID and nonce to the cookies file and reuses it if it's not empty, so you don't have to logout() every time
