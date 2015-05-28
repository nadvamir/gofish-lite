from random import randint
from math import floor

# a function to generate level map
def generate(maxDepth, width, height=1):
    lake = []
    # fill in the lake with ones
    for i in range(0, height):
        lake.append([])
    for i in range(0, height):
        for j in range(0, width):
            lake[i].append(1)

    # make holes
    for i in range(0, randint(3, 5 + height)):
        makeHole(lake, width, height, maxDepth)

    return lake

def makeHole(lake, w, h, maxDepth):
    # choose the pit
    x = randint(0, w-1)
    y = randint(0, h-1)

    # choose the depth
    d = randint(maxDepth / 2, maxDepth)

    # start spreading the hole
    digDown(lake, d, x, y, w, h)

def digDown(lake, d, x, y, w, h):
    if x < 0 or y < 0 or x >= w or y >= h:
        return
    if lake[y][x] >= d:
        return
    lake[y][x] = d
    digDown(lake, nextDepth(d), x, y-1, w, h)
    digDown(lake, nextDepth(d), x+1, y, w, h)
    digDown(lake, nextDepth(d), x, y+1, w, h)
    digDown(lake, nextDepth(d), x-1, y, w, h)

def nextDepth(d):
    return d - randint(0, 2)

