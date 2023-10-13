import sys, os, inspect, pygame
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import build

pygame.init()

class HouseBuilding:
    def __init__(self):
        self.image = pygame.image.load("graphics\\house.png")
        self.icon = pygame.image.load("graphics\\icons\\house.png")
        self.cost = build.buildingCost(
            {"steel" : 0, "stone" : 100, "wood" : 25, "food" : 0}
            )
