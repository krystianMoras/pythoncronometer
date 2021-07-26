import json


# what is not specified in the structure I couldn't identify but I'll leave it to future generations general pattern
# seems to be <uniqueid>,<lowercase name>,<db>,?,?,0,0,<full name>,<default serving id>,<default serving name>,
# <language>,<foodid>,?,?,?,? and between db and full name there are sometimes 5 numbers instead of 4 so I decided to
# pivot around double 0's
def extractFindFoodResponse(jsonResponse):
    text = jsonResponse[4:]  # cut OK//
    text = json.loads(text)
    structure = {
        1: "name",
        2: "serving id",
        3: "serving name",
        4: "language",
        5: "foodid",
        7: "category",
        10: "uniqueid?",
        11: "lowercase name",
        12: "db"
    }
    last = text[0]
    foodIDMap = {}
    diffFromLast = 9
    stringArray = text[-3]
   # print(stringArray)
    for i in range(1, len(text) - 5):
        if last == 0 and text[i] == 0 and diffFromLast > 12:
            diffFromLast = 0
            foodIDMap[stringArray[text[i + 1] - 1]] = text[i + 5]
        # print(text[i], end=" ")
        else:
            diffFromLast += 1
            # print(f"{structure.get(diffFromLast,'unidentified')}={text[i]}",end=" ")
            # if diffFromLast == 9:
            #    print()
            last = text[i]
    #print(len(foodIDMap))
    #print(foodIDMap)
    return foodIDMap
test = '[0,0,0,1,9942233,"BEZabz",455493,1000.0,4888786,0,0,2021,7,14,2,4,0,1,9942233,"BEZaNt",455493,1000.0,4888786,0,0,2021,7,14,2,4,0,1,9942233,"BEZaLi",455493,1000.0,4888786,0,0,2021,7,14,2,4,3,3,2021,7,14,2,0,1,["com.cronometer.client.data.DayInfo/469063487","com.cronometer.client.data.Day/1013293213","java.util.ArrayList/4159755760","com.cronometer.client.data.Serving/4179698402"],0,7]'
test2 = '[5,0,0,6,44516278,"BEgjF7",16191597,200.0,4888786,0,0,2021,7,16,2,4,0,5,999254,"BEgikL",450910,100.0,4888786,0,0,2021,7,16,2,4,0,4,999254,"BEgigM",450910,200.0,4888786,0,0,2021,7,16,2,4,4915289,3,1023977,"BEgieM",455522,300.0,4888786,0,0,2021,7,16,2,4,0,2,32810498,"BEghI1",463083,245.4375,4888786,0,0,2021,7,16,2,4,4915289,1,1080687,"BEghFF",455522,200.0,4888786,0,0,2021,7,16,2,4,6,3,2021,7,16,2,0,1,["com.cronometer.client.data.DayInfo/469063487","com.cronometer.client.data.Day/1013293213","java.util.ArrayList/4159755760","com.cronometer.client.data.Serving/4179698402","{\"servingTranslations\":[{\"id\":1149374789,\"tid\":4915289},{\"id\":1149380492,\"tid\":4915289}]}"],0,7]'
def extractDayInfoResponse(jsonResponse):
    #ugly but works, idk how to do it I get rid of subarray here because json decoder throws error
    jsonResponse = jsonResponse.split("[")[1][:-1]
    jsonResponse = "[" + jsonResponse + "]"
    #parsing
    jsonResponse = json.loads(jsonResponse)
    entries = []
    try:
        for i in range(4,len(jsonResponse),14):
            servingID = jsonResponse[i]
            alphabeticID = jsonResponse[i+1]
            foodID = jsonResponse[i+2]
            grams = jsonResponse[i+3]
            userID = jsonResponse[i+4]
            #hour = jsonResponse[i+5]
            #minute = jsonResponse[i+6]
            year = jsonResponse[i+7]
            month = jsonResponse[i+8]
            day = jsonResponse[i+9]
            # +4 unidentified numbers
            entryMap = {"servingID":servingID,"alphabeticID":alphabeticID,"foodID":foodID,"grams":grams,"userID":userID,"year":year,"month":month,"day":day}
            entries.append(entryMap)
    finally:
        return entries
targetTest = '[0,10009,0,134.3125,3,0,2,0,10008,45.0,3,2000.0,3,0,2,0,10005,150.0,3,1100.0,3,0,2,0,10004,30.0,3,0,0,2,0,10003,35.0,3,0,0,2,1,10002,17.0,3,0,0,2,1,10001,1.6,3,0,0,2,1,606,0.0,3,0,0,2,1,605,0.0,3,0,0,2,1,512,0.952543977798,3,0,0,2,1,510,1.6329325333680003,3,0,0,2,1,509,1.1226411166905002,3,0,0,2,1,508,1.1226411166905002,3,0,0,2,1,507,0.6463691277915,3,0,0,2,1,506,0.6463691277915,3,0,0,2,1,505,2.585476511166,3,0,0,2,1,504,2.8576319333940003,3,0,0,2,1,503,1.292738255583,3,0,0,2,1,502,1.3607771111400002,3,0,0,2,1,501,0.34019427778500005,3,0,0,2,1,430,120.0,3,2000.0,3,0,2,0,421,550.0,3,3500.0,3,0,2,1,418,2.4,3,0,0,2,1,417,400.0,3,1000.0,3,0,2,1,415,1.3,3,100.0,3,0,2,1,410,5.0,3,0,0,2,1,406,16.0,3,35.0,3,0,2,1,405,1.3,3,0,0,2,1,404,1.2,3,0,0,2,1,401,90.0,3,2000.0,3,0,2,1,324,600.0,3,4000.0,3,0,2,1,323,15.0,3,1000.0,3,0,2,0,319,0,3000.0,3,0,2,1,318,3000.0,3,0,0,2,1,317,55.0,3,400.0,3,0,2,1,315,2.3,3,11.0,3,0,2,0,313,4000.0,3,10000.0,3,0,2,1,312,0.9,3,10.0,3,0,2,1,309,11.0,3,40.0,3,0,2,1,307,1500.0,3,2300.0,3,0,2,1,306,3400.0,3,0,0,2,1,305,700.0,3,4000.0,3,0,2,1,304,420.0,3,0,0,2,1,303,8.0,3,45.0,3,0,2,1,301,1000.0,3,2500.0,3,0,2,1,291,38.0,3,0,0,2,1,255,3700.0,3,0,0,2,1,208,1537.0,3,2149.0,3,0,2,1,205,130.0,3,0,0,2,1,204,65.0,3,0,0,2,1,203,56.0,3,0,0,2,1,-1205,130.0,3,0,0,2,52,1,["java.util.ArrayList/4159755760","com.cronometer.client.data.Target/3864382316","java.lang.Double/858496421"],0,7]'
def extractTargets(jsonResponse):
    jsonResponse = json.loads(jsonResponse)
    for i in range(1,len(jsonResponse),7):
        print(jsonResponse[i:i+7])
customFoodsTest = '[0,0,0,-3,0,0,1,17,0,0,0,16312278,0,0,2,0,0,0,-3,0,0,1,16,0,0,0,16306714,0,0,2,0,0,0,-3,0,0,1,15,0,0,0,16306084,0,0,2,0,0,0,-3,0,0,0,14,0,0,0,16192546,0,0,2,0,0,0,-3,0,0,0,13,0,0,0,16192526,0,0,2,0,0,0,-3,0,0,0,12,0,0,0,16192473,0,0,2,0,0,0,-3,0,0,0,11,0,0,0,16192113,0,0,2,0,0,0,-3,0,0,0,10,0,0,0,16192095,0,0,2,0,0,0,-3,0,0,0,9,0,0,0,16192089,0,0,2,0,0,0,-3,0,0,1,8,0,0,0,16191635,0,0,2,0,0,0,-3,0,0,0,7,0,0,0,16191610,0,0,2,0,0,0,-3,0,0,0,6,0,0,0,16191605,0,0,2,0,0,0,-3,0,0,0,5,0,0,0,16191599,0,0,2,0,0,0,5,4,0,0,0,3,0,0,0,16191597,0,0,2,14,1,["[Lcom.cronometer.client.data.SearchHit;/1332236557","com.cronometer.client.data.SearchHit/3466102008","TestFood1","com.cronometer.client.data.Source/2927124550","TestFood2","TestFood3","TestFood4","TestRecipe1","Food1","Food2","Food3","test1","test2","test3","Penne with dried tomatoes, feta and spinach","Sandwich with salami, canembert, tomato, cucumber and kale sprouts","TestRecipe2"],0,7]'
def extractCustomFoods(jsonResponse):
    foods = {}
    jsonResponse = json.loads(jsonResponse[4:])
    numOfFoods = jsonResponse[-5]
    for i in range(0,15*(numOfFoods-1),15):
        isRecipe = jsonResponse[i+6] == 1
        namePointer = jsonResponse[i+7]
        foodID = jsonResponse[i + 11]
        #print(jsonResponse[-3][namePointer-1],foodID)
        foods[jsonResponse[-3][namePointer-1]] = foodID
        #print(jsonResponse[i:i+15])
    i+=15
    isRecipe = jsonResponse[i + 7] == 1
    namePointer = jsonResponse[i + 8]
    foodID = jsonResponse[i + 12]
    foods[jsonResponse[-3][namePointer - 1]] = foodID
    #print(jsonResponse[-3][namePointer - 1], foodID)
    return foods




