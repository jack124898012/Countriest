from buildings import *
import build
import ast
import pygame
from maps import default
from image import *

pygame.init()

builds = {-1 : bulldoze, 0 : test, 1 : b_house, 2 : b_bakery,
3 : b_downleft, 4 : b_downright,
             5 : b_horizontal, 6 : b_leftdown, 7 : b_rightdown,
          8 : b_vertical, 9 : appletree_1,
          bulldoze : -1, test : 0, b_house : 1, b_bakery : 2,
          b_downleft : 3, b_downright : 4,
             b_horizontal : 5, b_leftdown : 6, b_rightdown : 7,
b_vertical : 8, appletree_0 : 9}

def getTile(loaded_map, x, y):
    for c in loaded_map:
        if c[0] == x and c[1] == y:
            return builds[c[2]]
    return builds[0]

# tiles = [(x, y, type), (x, y, type)]
# size = (x, y)
def saveMap(name, size, tiles):
    if type(tiles) != list: tiles = list(tiles)
    tiles = [size] + tiles
    file = open("maps\\" + str(name), "w")
    for x in range(len(tiles)):
        tiles[x] = list(tiles[x])
        #if len(tiles[x]) == 3:
            #print(tiles[x][2])
            #tiles[tiles.index(x)][2] = builds[tiles[tiles.index(x)][2]]
        file.write(str(tiles[x]) + ";")
    file.close()

def nearbyTiles(loaded_map, x, y):
    return [getTile(loaded_map, x+1, y), getTile(loaded_map, x, y-1), getTile(loaded_map, x, y+1), getTile(loaded_map, x-1, y)]

def getMap(name):
    try:
        open("maps\\" + str(name), "r").close()
    except:
        open("maps\\" + str(name), "w").close()
    file = open("maps\\" + str(name), "r")
    lines = file.readlines()
    for x in lines:
        x.replace("\n", "")
    file.close()
    tiles = ""
    for x in lines: tiles += x
    tiles = tiles.split(";")
    for x in range(len(tiles)):
        try:
            tiles[x] = ast.literal_eval(tiles[x])
        except:
            continue
    for a in range(len(tiles)):
        tile = []
        for b in tiles[a]:
            tile.append(b)
    size = tiles.pop(0)
    tiles.pop()
    for tile in tiles:
        if len(tile) == 3:
            for num, te in builds.items():
                if num == tile[2]:
                    tile[2] == builds[num]
                    break
    output = [size, tiles]
    return output
#saveMap("map.map", (2, 2), [[1, 1, 0], [1, 2, 0], [2, 1, 0], [2, 2, 0]]) # todo: make input size, set(set(x, y, tile))
#print(getMap("map.map"))
#print(default.make((4, 4)))
#saveMap("t.map", (4, 4), default.make((4, 4))[1])
