def make(size):
    tiles = []
    for x in range(1, size[0]+1):
        for y in range(1, size[1]+1):
            tiles.append([x, y, 0])
    tiles = tiles
    return tiles
