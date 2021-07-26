from constants import nutrientIds


class Food:
    def __init__(self):
        self.nutrientMap = {}
        self.servingsList = []
        self.ingredients = {}
        self.name = ""
        self.nutrientMap["fatsPercent"] = 0
        self.nutrientMap["alcoholPercent"] = 0
        self.nutrientMap["carbsPercent"] = 0
        self.nutrientMap["carbs.2?"] = 0
        self.nutrientMap["proteinPercent"] = 0

    def _findStrings(self, array):
        # find all strings and return their positions
        # they are unique ids of ingredients and food itself
        strings = []
        for i in range(len(array)):
            if type(array[i]) is str:
                strings.append(i)
        return strings

    def _calculateNutrientsStart(self, array, pivot):
        numOfServings = array[pivot - 2]
        numOfNutrients = array[pivot - 8 - 7 * numOfServings - 2 + 7 - 2]
        return pivot - 8 - 7 * numOfServings - 2 + 7 - 2 - 4 * numOfNutrients

    # def convertToGWT(self):
    #     gwtString = ""
    #     reverseNutrientIds = {v: k for k, v in nutrientIds.items()}
    #     numofnutrients = len(self.nutrientMap)
    #     gwtString += str(numofnutrients) + "|"
    #     somenumber = 16
    #     for i in range(numofnutrients):
    #         gwtString += str(somenumber) + "|"
    #
    #         gwtString += str(reverseNutrientIds[list(self.nutrientMap.keys())[i]]) + "|"
    #         gwtString += str(somenumber + 1) + "|"
    #         gwtString += str(int(list(self.nutrientMap.values())[i])) + "|"
    #     return gwtString

    def _getNutrients(self, array, strings):
        i = self._calculateNutrientsStart(array, strings[-1])
        counter = 0
        for j in range(i, len(array), 4):
            if type(array[j]) == int and counter == array[j]:
                break
            x = nutrientIds.get(array[j + 2], 'not found')
            if x != "not found":
                counter += 1
                self.nutrientMap[x] = array[j]

    def _getServings(self, array, strings):
        pivot = strings[-1]
        numOfServings = array[pivot - 2]
        servingsStart = pivot - 8 - 7 * numOfServings - 2 + 7
        last = servingsStart
        for j in range(servingsStart, pivot - 2 - 8, 7):
            serving = Serving()
            serving.weight = array[j]
            serving.id = array[j + 3]
            serving.name = str(array[j + 5]).strip(".0")
            serving.pointerToName = array[j + 2] - 1
            self.servingsList.append(serving)
            last = j + 7
        j = last
        #
        serving = Serving()
        serving.weight = array[j]
        serving.id = array[j + 4]
        serving.name = str(array[j + 6]).strip(".0")
        serving.pointerToName = array[j + 3] - 1
        self.servingsList.append(serving)

        subarray = array[len(array) - 3]
        self.name = subarray[-1]
        uniques = []
        for serving in self.servingsList:

            if serving.name == "1":
                serving.name = subarray[serving.pointerToName]
            else:
                serving.name += " " + subarray[serving.pointerToName]
            if serving.name not in [x.name for x in uniques]:
                uniques.append(serving)
        self.servingsList = uniques

    def _getIngredients(self, array, strings):

        if len(strings) < 2:
            return  # no ingredients
        # last string is id of food itself, omit it
        for string in strings[:-1]:
            servingID = array[string - 1]
            foodID = array[string + 1]
            weight = array[string + 2]
            self.ingredients[foodID] = (servingID, weight)

    def jsonToFood(self, array):
        strings = self._findStrings(array)
        self._getNutrients(array, strings)
        self._getServings(array, strings)
        self._getIngredients(array, strings)

        return self

    def __repr__(self):
        return f"{self.name} \n Ingredients: {self.ingredients} \n Nutrients: {self.nutrientMap} \n Servings: {self.servingsList} "


class Serving:
    def __init__(self):
        self.id = None
        self.name = None
        self.weight = None
        self.pointerToName = None

    def __repr__(self):
        return f"ServingId={self.id} Name=\"{self.name}\" Weight={self.weight}g"
