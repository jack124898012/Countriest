class Build:
    def __init__(self, buildingType, x, y):
        self.buidling = buildingType
        self.x = x
        self.y = y

class buildingType:
    def __init__(self, buildingType):
        self.__building = buildingType
    def getType():
        return self.__building

class buildingCost:
    def __init__(self, resources):
        self.steel = resources["steel"]
        self.stone = resources["stone"]
        self.wood = resources["wood"]
        self.food = resources["food"]
        self.resources = resources
