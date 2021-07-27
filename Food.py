from constants import nutrientIds


class Food:
    def __init__(self):
        self.nutrientMap = {}
        self.servingsList = []
        self.ingredients = {}
        self.name = "pythoncronometerplaceholder"
        self.id = -1
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

    def _getNutrients(self, array, strings):
        i = self._calculateNutrientsStart(array, strings[-1])
        counter = 0
        for j in range(i, len(array), 4):
            if type(array[j]) == int and counter == array[j]:
                break
            x = nutrientIds.get(array[j + 2], 'not found')
            if x != "not found":
                counter += 1
                self.nutrientMap[array[j + 2]] = array[j]

    def _modifyNutrients(self, recipeSize):
        self.nutrientMap = {nutrient[0]: nutrient[1] * 100 / recipeSize for nutrient in self.nutrientMap.items()}

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
        # if its a recipe multiply nutrients by array[j]/100
        if len(strings) > 1:
            self._modifyNutrients(array[j])
        serving.weight = array[j]
        serving.id = array[j + 4]
        serving.name = str(array[j + 6]).strip(".0")
        serving.pointerToName = array[j + 3]
        self.servingsList.append(serving)

        subarray = array[len(array) - 3]
        self.name = subarray[-1]
        # uniques = []
        for serving in self.servingsList:

            if serving.name == "1":
                serving.name = subarray[serving.pointerToName]
            else:
                serving.name += " " + subarray[serving.pointerToName]

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

    def ingredientsToGWT(self):
        string = str(len(self.ingredients)) + "|"

        for ingredient in self.ingredients.items():
            string += f"17|{ingredient[1][1]}|{ingredient[0]}|A|{ingredient[1][0]}|0|0|"
        string += "0"
        return string

    def addIngredient(self, foodID, servingID, weight):
        self.ingredients[foodID] = (servingID, weight)

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
