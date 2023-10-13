import sys, os, inspect, pygame
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import build

pygame.init()

class TreeBuilding:
    def __init__(self):
        self.cost = build.buildingCost(
            {"steel" : 0, "stone" : 0, "wood" : 50, "food" : 10}
            )
