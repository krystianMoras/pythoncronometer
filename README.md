# pythoncronometer
Since Cronometer won't release API this python library allows to communicate with Cronometer without going through their site.

If Cronometer team does not want this to be public feel free to contact me.
# Usage

Create a cookies.txt (I'll fix it next push)
Start a client
```
session = requests.Session()
client = Client(session)
```
Login to the cronometer
```
client.login("username","password")
```
Add meal to diary
e.g. add 1000 ml of tap water on 6th July 2021
```
#client.addServing(year,month,day,foodID,servingID,grams)
client.addServing(2021,7,6,455493,9942233,1000)
```
To obtain serving ID and food ID you can use following methods
```
print(client.findFood("tap water",5))
#{'Tea, Black, Brewed, Prepared with Tap Water': 7027, 'Beverages, Water, Tap, Municipal': 6646, 'Beverages, Water, Tap, Drinking': 6643, 'Beverages, Water, Tap, Well': 6640, 'Tap Water': 455493}
print(client.getFood(455493).servingsList[0])
#ServingId=9942233 Name="mL" Weight=1.0g
```
You can also export daily summary and servings
```
exported = StringIO(client.exportDailyServings("2021-07-13","2021-07-13"))
df = pandas.read_csv(exported)
print(df)
```
Logout
```
client.logout()
```
Note: login() saves your userID and nonce to the cookies.txt and reuses it if it's not empty, so you don't have to logout() every time
