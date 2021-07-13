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
