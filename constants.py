# GWT constants
GWTHeader = "0DC85D54E7772402C7AA34F8F9193902"
GWTAUTH = f"7|0|5|https://cronometer.com/cronometer/|{GWTHeader}|com.cronometer.client.CronometerService|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|"
gwtHeaders = {"content-type": "text/x-gwt-rpc; charset=UTF-8",
              "x-gwt-module-base": "https://cronometer.com/cronometer/",
              "x-gwt-permutation": "7B121DC5483BF272B1BC1916DA9FA963"}
GWTGenerateAuthFormat = GWTGenerateAuthToken = "7|0|8|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|generateAuthorizationToken|java.lang.String/2004016611|I|com.cronometer.client.data.AuthScope/3337242207|{nonce}|1|2|3|4|4|5|6|6|7|8|{userid}|3600|7|2|"
GWTLogoutFormat = "7|0|6|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|logout|java.lang.String/2004016611|{nonce}|1|2|3|4|1|5|6|"
GWTGetFoodFormat = "7|0|7|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|getFood|java.lang.String/2004016611|I|{nonce}|1|2|3|4|2|5|6|7|{foodID}|"
GWTAddServingFormat = "7|0|9|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|addServing|java.lang.String/2004016611|com.cronometer.client.data.Serving/4179698402|I|{nonce}|com.cronometer.client.data.Day/1013293213|1|2|3|4|3|5|6|7|8|6|9|{day}|{month}|{year}|0|0|0|{grams}|{foodID}|A|{servingID}|1|0|{userid}|"
GWTFindFoodFormat = "7|0|10|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|findFoods|java.lang.String/2004016611|I|com.cronometer.client.data.Source/2927124550|com.cronometer.client.widgets.FoodSearchPanel$FoodSearchTabSelection/3991074765|{nonce}|{query}|1|2|3|4|7|5|5|6|7|6|5|8|9|10|{number_of_suggestions}|7|0|0|0|8|0|"
GWTGetDayInfoFormat = "7|0|8|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|getDayInfo|java.lang.String/2004016611|com.cronometer.client.data.Day/1013293213|I|{nonce}|1|2|3|4|3|5|6|7|8|6|{day}|{month}|{year}|{userid}|"
GWTEditServingFormat = "7|0|9|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|editServing|java.lang.String/2004016611|com.cronometer.client.data.Serving/4179698402|I|{nonce}|com.cronometer.client.data.Day/1013293213|1|2|3|4|3|5|6|7|8|6|9|{day}|{month}|{year}|0|0|0|{grams}|{foodID}|{alphabeticid}|{servingid}|{i}|{uniqueid}|{userid}|"
GWTDeleteServingFormat = "7|0|8|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|removeServing|java.lang.String/2004016611|J|I|{nonce}|1|2|3|4|3|5|6|7|8|{alphabeticid}|{userid}|"
GWTAddFoodFormat = "7|0|25|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|addFood|java.lang.String/2004016611|com.cronometer.client.data.Food/173541194|com.cronometer.client.foodeditor.IngredientSubstitutions/53890574|d9e19e382aa2579d8819b953cd6a9ab4|java.util.ArrayList/4159755760||com.cronometer.client.data.NutritionLabelType/1252743626|com.cronometer.client.data.Measure/2801078263|Serving|com.cronometer.client.data.Measure$Type/1842092880|java.util.HashMap/1797211028|java.lang.Integer/3438268394|java.lang.Double/858496421|Custom|java.util.HashSet/3273092938|com.cronometer.client.data.Translation/2027684045|com.cronometer.client.data.Language/4060169223|en|English|https://cdn1.cronometer.com/media/flags/us.png|{name}|1|2|3|4|3|5|6|7|8|6|0|9|0|0|10|0|0|0|11|0|A|9|1|12|1|0|0|13|14|2|100|15|{nutrientsString}15|0|0|0|18|19|0|9|1|20|21|22|23|24|23|25|0|{userid}|0|"
GWTFindMyFoodsFormat = "7|0|6|https://cronometer.com/cronometer/|" + GWTHeader + "|com.cronometer.client.CronometerService|findMyFoods|java.lang.String/2004016611|{nonce}|1|2|3|4|1|5|6|"
# GWT urls
GWTBaseURL = "https://cronometer.com/cronometer/app"
# Urls
exportURL = "https://cronometer.com/export"
loginPageURL = "https://cronometer.com/login/"
regularHeaders = {"Content-Type": "application/x-www-form-urlencoded",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
loginRequestURL = "https://cronometer.com/login"

nutrientIds = {208: "energy",
               221: "alcohol",
               207: "ash",
               10011: "beta-hydroxybutyrate",
               262: "caffeine",
               255: "water",
               205: "carbs",
               291: "fiber",
               209: "starch",
               269: "sugars",
               10010: "allulose",
               212: "fructose",
               287: "galactose",
               211: "glucose",
               213: "lactose",
               214: "maltose",
               210: "sucrose",
               10009: "added suggars",
               10007: "sugar alcohol",
               204: "fat",
               645: "monounsaturated",
               646: "polyunsaturated",
               10001: "omega-3",
               10002: "omega-6",
               606: "saturated",
               605: "trans-fats",
               601: "cholesterol",
               636: "phytosterol",
               203: "protein",
               513: "alanine",
               511: "arginine",
               514: "aspartic acid",
               507: "cystine",
               515: "glutamic acid",
               516: "glycine",
               512: "histidine",
               521: "hydroxyproline",
               503: "isoleucine",
               504: "leucine",
               505: "lysine",
               506: "methionine",
               508: "phenyalanine",
               517: "proline",
               518: "serine",
               502: "threonine",
               501: "thryptophan",
               509: "tyrosine",
               510: "valine",
               404: "b1",
               405: "b2",
               406: "b3",
               410: "b5",
               415: "b6",
               418: "b12",
               10004: "biotin",
               421: "choline",
               417: "folate",
               318: "vitamin a",
               322: "alpha-carotene",
               321: "beta-carotene",
               334: "beta-cryptoxanthin",
               338: "lutein+zeaxanthin",
               337: "lycopene",
               319: "retinol",
               320: "retinol activity equivalent",
               401: "vitamin c",
               324: "vitamin d",
               323: "vitamin e",
               341: "beta tocopherol",
               343: "delta tocopherol",
               342: "gamma tocopherol",
               430: "vitamin k",
               301: "calcium",
               10003: "chromium",
               312: "copper",
               313: "fluoride",
               10005: "iodine",
               303: "iron",
               304: "magnesium",
               315: "manganese",
               10008: "molybdenum",
               305: "phosphorus",
               306: "potassium",
               317: "selenium",
               307: "sodium",
               309: "zinc",
               -204:"fatsPercent",
               -221:"alcoholPercent",
               -205:"carbsPercent",
               -1205:"carbs.2?",
               -203:"proteinPercent"
               }
