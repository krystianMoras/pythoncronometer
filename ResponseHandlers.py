import json

from constants import nutrientIds
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
targetTest = '[0,10009,0,161.125,3,0,2,0,10008,45.0,3,2000.0,3,0,2,0,10005,150.0,3,1100.0,3,0,2,0,10004,30.0,3,0,0,2,0,10003,35.0,3,0,0,2,1,10002,17.0,3,0,0,2,1,10001,1.6,3,0,0,2,1,606,0.0,3,0,0,2,1,605,0.0,3,0,0,2,1,512,1.092,3,0,0,2,1,510,1.872,3,0,0,2,1,509,1.2870000000000001,3,0,0,2,1,508,1.2870000000000001,3,0,0,2,1,507,0.741,3,0,0,2,1,506,0.741,3,0,0,2,1,505,2.964,3,0,0,2,1,504,3.2760000000000002,3,0,0,2,1,503,1.482,3,0,0,2,1,502,1.56,3,0,0,2,1,501,0.39,3,0,0,2,1,430,120.0,3,2000.0,3,0,2,0,421,550.0,3,3500.0,3,0,2,1,418,2.4,3,0,0,2,1,417,400.0,3,1000.0,3,0,2,1,415,1.3,3,100.0,3,0,2,1,410,5.0,3,0,0,2,1,406,16.0,3,35.0,3,0,2,1,405,1.3,3,0,0,2,1,404,1.2,3,0,0,2,1,401,90.0,3,2000.0,3,0,2,1,324,600.0,3,4000.0,3,0,2,1,323,15.0,3,1000.0,3,0,2,0,319,0,3000.0,3,0,2,1,318,3000.0,3,0,0,2,1,317,55.0,3,400.0,3,0,2,1,315,2.3,3,11.0,3,0,2,0,313,4000.0,3,10000.0,3,0,2,1,312,0.9,3,10.0,3,0,2,1,309,11.0,3,40.0,3,0,2,1,307,1500.0,3,2300.0,3,0,2,1,306,3400.0,3,0,0,2,1,305,700.0,3,4000.0,3,0,2,1,304,400.0,3,0,0,2,1,303,8.0,3,45.0,3,0,2,1,301,1000.0,3,2500.0,3,0,2,1,291,38.0,3,0,0,2,1,255,3700.0,3,0,0,2,1,208,1840.0,3,2578.0,3,0,2,1,205,130.0,3,0,0,2,1,204,65.0,3,0,0,2,1,203,56.0,3,0,0,2,1,-1205,130.0,3,0,0,2,52,1,["java.util.ArrayList/4159755760","com.cronometer.client.data.Target/3864382316","java.lang.Double/858496421"],0,7]'
def extractTargets(jsonResponse):
    jsonResponse = json.loads(jsonResponse)
    targets = {}
    nutrientPointers = []
    for i in range(len(jsonResponse)):
        if type(jsonResponse[i]) == int and jsonResponse[i] in nutrientIds.keys():
            nutrientPointers.append(i)
    #targets[jsonResponse[nutrientPointers[0]]] = (jsonResponse[nutrientPointers[0] + 1],jsonResponse[nutrientPointers[0] + 2])
    targets[jsonResponse[nutrientPointers[0]]] = jsonResponse[nutrientPointers[0] + 1]
   # print(nutrientIds[jsonResponse[nutrientPointers[0]]], f"Min:{jsonResponse[nutrientPointers[0] + 1]}",f"Max:{jsonResponse[nutrientPointers[0] + 2]}")

    for nutrientPointer in nutrientPointers[1:]:
        #targets[jsonResponse[nutrientPointer]] = (jsonResponse[nutrientPointer + 1], jsonResponse[nutrientPointer + 3])
        targets[jsonResponse[nutrientPointer]] = jsonResponse[nutrientPointer + 1]

    #    print(nutrientIds[jsonResponse[nutrientPointer]],f"Min:{jsonResponse[nutrientPointer+1]}",f"Max:{jsonResponse[nutrientPointer+3]}")


    return targets

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

authInfoTest = r'[4888786,1,1,0,78.0,0,2021,7,25,2,5,68.0388,0,2021,7,12,2,5,2,4,3,66,0,1,255,3700.0,65,0,0,64,255,63,1,510,1.872,65,0,0,64,510,63,1,509,1.2870000000000001,65,0,0,64,509,63,1,508,1.2870000000000001,65,0,0,64,508,63,1,507,0.741,65,0,0,64,507,63,1,506,0.741,65,0,0,64,506,63,1,505,2.964,65,0,0,64,505,63,1,504,3.2760000000000002,65,0,0,64,504,63,1,503,1.482,65,0,0,64,503,63,1,502,1.56,65,0,0,64,502,63,1,501,0.39,65,0,0,64,501,63,1,606,0.0,65,0,0,64,606,63,1,605,0.0,65,0,0,64,605,63,1,208,1840.0,65,2578.0,65,0,64,208,63,1,205,130.0,65,0,0,64,205,63,1,204,65.0,65,0,0,64,204,63,1,203,56.0,65,0,0,64,203,63,1,324,600.0,65,4000.0,65,0,64,324,63,1,323,15.0,65,1000.0,65,0,64,323,63,0,319,0,3000.0,65,0,64,319,63,1,318,3000.0,65,0,0,64,318,63,1,317,55.0,65,400.0,65,0,64,317,63,1,315,2.3,65,11.0,65,0,64,315,63,0,313,4000.0,65,10000.0,65,0,64,313,63,1,312,0.9,65,10.0,65,0,64,312,63,1,309,11.0,65,40.0,65,0,64,309,63,1,-1205,130.0,65,0,0,64,-1205,63,1,307,1500.0,65,2300.0,65,0,64,307,63,1,306,3400.0,65,0,0,64,306,63,1,305,700.0,65,4000.0,65,0,64,305,63,1,304,400.0,65,0,0,64,304,63,1,303,8.0,65,45.0,65,0,64,303,63,1,430,120.0,65,2000.0,65,0,64,430,63,1,301,1000.0,65,2500.0,65,0,64,301,63,0,421,550.0,65,3500.0,65,0,64,421,63,1,291,38.0,65,0,0,64,291,63,1,418,2.4,65,0,0,64,418,63,1,417,400.0,65,1000.0,65,0,64,417,63,1,415,1.3,65,100.0,65,0,64,415,63,1,410,5.0,65,0,0,64,410,63,0,10009,0,161.125,65,0,64,10009,63,0,10008,45.0,65,2000.0,65,0,64,10008,63,1,406,16.0,65,35.0,65,0,64,406,63,0,10005,150.0,65,1100.0,65,0,64,10005,63,1,405,1.3,65,0,0,64,405,63,0,10004,30.0,65,0,0,64,10004,63,1,404,1.2,65,0,0,64,404,63,0,10003,35.0,65,0,0,64,10003,63,1,10002,17.0,65,0,0,64,10002,63,1,10001,1.6,65,0,0,64,10001,63,1,401,90.0,65,2000.0,65,0,64,401,63,1,512,1.092,65,0,0,64,512,63,52,7,0,0,62,0,5,61,60,"A",0,0,7,0,11,0,"A",0,59,9,58,9,20,9,57,9,29,9,56,9,55,9,54,9,53,9,52,9,20,9,51,9,20,9,50,9,29,9,49,9,48,9,47,9,46,9,45,9,29,9,44,9,43,9,42,9,41,9,40,9,39,9,38,9,37,9,36,9,35,9,34,9,33,9,32,9,31,9,30,9,29,9,28,9,27,9,26,9,25,9,24,9,20,9,23,9,22,9,21,9,20,9,19,9,18,9,17,9,16,9,15,9,26,7,0,-1,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,14,0,"A","XrhwLYI",0,4888786,13,1,0,0,0,0,12,0,11,0,10,9,1,8,0,7,6,0,4,0,4888786,13,8,0,12.0,0,2021,7,25,2,5,1,4,3,2001,10,6,2,"Xqe71GQ",1,["com.cronometer.client.data.User/1559089151","com.cronometer.client.data.Day/1013293213","com.cronometer.client.data.BiometricHistory/241919215","java.util.ArrayList/4159755760","com.cronometer.client.data.DataPoint/1988084281","vocav31906@eyeremind.com","java.util.HashMap/1797211028","java.util.HashSet/3273092938","java.lang.String/2004016611","prod","java.util.LinkedList/3953877921","com.cronometer.client.data.Gender/3477708896","cdcd842c611c8369f724eb5031b6ac30","com.cronometer.client.data.targets.MacroTargetsContext/1323636377","calories.activity","0.375","macroLipids","30","show.new.exercise.switch","true","heightInCM","184","l2","tz","120","weightInKG","68.038855557","fasting","false","macroProtein","25","preferred.unit.1","1","wg","85","group.subtotal","macros","macroIndex","6","heightUnit","Centimeters","sas","1626164126604","targets.macros.sugaralcohol","macroCarbs","45","ad1","48","use.thermic.effect.food","email.validated","new.exercise","weightGoal","0.25","customCharts","{\"chart_system\":{\"chrt_cc\":{\"fast\":true,\"on\":true,\"zoom\":false,\"daytype\":0,\"time\":2,\"left_unit\":0,\"right_unit\":0,\"incl_tod\":true,\"target_line\":true,\"cus_index\":0,\"trend\":false},\"chrt_sm\":{\"fast\":true,\"on\":true,\"zoom\":true,\"daytype\":0,\"time\":2,\"left_unit\":1,\"right_unit\":0,\"incl_tod\":true,\"target_line\":true,\"cus_index\":1,\"trend\":false,\"series\":[{\"side\":\"LEFT\",\"type\":\"metric\",\"id\":1}]}}}","targets.macros.macros.grams","targets.include.exercises","weightUnit","Kilograms","4b07290f0021f0aaa507c2cc87951227","com.cronometer.client.data.LoginSite/3433773684","com.cronometer.client.data.ReproductiveStatus/2020709890","java.lang.Integer/3438268394","com.cronometer.client.data.Target/3864382316","java.lang.Double/858496421","Europe/Berlin"],0,7]'
def extractAuthInfo(jsonResponse):
    jsonResponse = json.loads(jsonResponse)
    for line in jsonResponse:
        if type(line) ==list:
            activity = line[line.index("calories.activity") + 1]
            macroLipids = line[line.index("macroLipids") + 1]
            macroProtein = line[line.index("macroProtein") + 1]
            macroCarbs = line[line.index("macroCarbs") + 1]
            return activity,macroCarbs,macroProtein,macroLipids




