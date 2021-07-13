from constants import nutrientIds


class Food:
    def __init__(self):
        self.nutrientMap = {}
        self.servingsList = []

    def _calculatePivot(self, array):
        pivot = -1
        for i in range(len(array)):
            if str(array[i]).startswith("X"):
                pivot = i
                break
        numOfServings = array[pivot - 2]
        numOfNutrients = array[pivot - 8 - 7 * numOfServings - 2 + 7 - 2]
        return pivot - 8 - 7 * numOfServings - 2 + 7 - 2 - 4 * numOfNutrients

    def _getNutrients(self, array, i):
        counter = 0
        for j in range(i, len(array), 4):
            if type(array[j]) == int and counter == array[j]:
                break
            x = nutrientIds.get(array[j + 2], 'not found')
            if x != "not found":
                counter += 1
                self.nutrientMap[x] = array[j]



    def _getServings(self, array):
        pivot = -1

        for k in range(len(array)):
            if str(array[k]).startswith("X"):
                pivot = k
        numOfServings = array[pivot - 2]
        resultantBeginning = pivot - 8 - 7 * numOfServings - 2 + 7
        last = resultantBeginning
        for j in range(resultantBeginning, pivot - 2 - 8, 7):
            serving = Serving()
            serving.weight = array[j]
            serving.id = array[j + 3]
            serving.name = str(array[j + 5]).strip(".0")
            serving.pointerToName = array[j + 2] - 1
            self.servingsList.append(serving)
            last = j+7


        j = last
        #
        serving = Serving()
        serving.weight = array[j]
        serving.id = array[j + 4]
        serving.name = str(array[j + 6]).strip(".0")
        serving.pointerToName = array[j + 3] - 1
        self.servingsList.append(serving)

    def jsonToFood(self, array):
        pivot = self._calculatePivot(array)
        self._getNutrients(array, pivot)
        self._getServings(array)
        subarray = array[len(array) - 3]
        uniques = []
        for serving in self.servingsList:

            if serving.name =="1":
                serving.name = subarray[serving.pointerToName]
            else:
                serving.name += " " + subarray[serving.pointerToName]
            if serving.name not in [x.name for x in uniques]:
                uniques.append(serving)
        self.servingsList = uniques
        return self

    def __repr__(self):
        return f"Nutrients:{self.nutrientMap} \n Servings: {self.servingsList}"


class Serving:
    def __init__(self):
        self.id = None
        self.name = None
        self.weight = None
        self.pointerToName = None

    def __repr__(self):
        return f"ServingId={self.id} Name=\"{self.name}\" Weight={self.weight}g"
