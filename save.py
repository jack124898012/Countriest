import mapmanager

def update(name, tiles):
    size = tiles[0]
    tiles = tiles[1]
    mapmanager.saveMap(name, size, tiles)
    return mapmanager.getMap(name)
