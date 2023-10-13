import sys, os, inspect, pygame
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import build

pygame.init()

class RoadBuilding:
    def __init__(self):
        self.cost = build.buildingCost(
            {"steel" : 10, "stone" : 10, "wood" : 0, "food" : 0}
            )
