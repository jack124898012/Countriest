import os

def getMaps():
    path = os.getcwd() + "\\maps"
    f = [files for r,d, files in os.walk(path)]
    maps = []
    for tmp in f[0]:
        if ".map" in tmp:
            maps.append(tmp)
    return maps
