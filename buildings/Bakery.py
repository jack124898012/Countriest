import sys, os, inspect, pygame
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import build

pygame.init()

class BakeryBuilding:
    def __init__(self):
        self.image = pygame.image.load("graphics\\bakery.png")
        self.icon = pygame.image.load("graphics\\icons\\bakery.png")
        self.cost = build.buildingCost(
            {"steel" : 100, "stone" : 100, "wood" : 125, "food" : 0}
            )
