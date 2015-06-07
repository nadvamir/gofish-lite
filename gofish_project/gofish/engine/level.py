from gamedef import *
from random import gauss
from random import randint
from random import random
from math import exp
import maps

# cost of unlocking given level
def cost(index):
    if 0 == index:
        return 0
    times = LEVELS[index-1]['toPlay']
    # times to play x optimal earnings for each weather group
    optE = sum([optEarnings(index-1, i) for i in range(0, len(WEATHER))])
    return int(IMPLIED_PERF * times * optE)

# a level object
def get(index):
    weather = randint(0, len(WEATHER)-1)
    gameMap = maps.generate(LEVELS[index]['maxdepth'], MAP_SIZE)
    return {
        'index': index,
        'name': LEVELS[index]['name'],
        'boat': LEVELS[index]['boat'],
        'weather': weather,
        'map': gameMap,
        'position': 0,
        'time': 0,
        'totalTime': TOTAL_TIME,
        'timeInLoc': [0 for i in range(0, MAP_SIZE)],
        'yields': getYields(index, weather, gameMap[0])
    }

# move cost in this level
def moveC(index):
    return BOATS[LEVELS[index]['boat']]['mult']

# optimal earnings in an average game
def optEarnings(index, weather):
    vf = valueF(index, weather)
    w = WEATHER[weather]['mult']
    b = moveC(index)
    optT = w * b / 2 - b
    optE = sum([vf(i) for i in range(1, int(optT)+1)])
    return int(optE * TOTAL_TIME / (optT + b)) # a very rough estimate

# fish value function for a game with given parameters
def valueF(index, weather):
    w = WEATHER[weather]['mult']
    b = moveC(index)
    v = topValue(index)
    return lambda x: v * exp(-2 * x / b / (w-2))

# top value for a fish
def topValue(index):
    return INIT_VAL + BASE_VAL ** index

# generate all yields, map is a 1d array of depths
def getYields(index, weather, gameMap):
    return [genYield(index, weather, d) for d in gameMap]

# generate a yield
def genYield(index, weather, depth):
    vf = valueF(index, weather)
    return [getFish(index, vf, i, depth) for i in range(1, TOTAL_TIME+1)]

# get a particular fish
def getFish(index, vf, i, depth):
    refVal = vf(1) / CHANCE_FISH
    val = vf(i)

    # value needs to be normalised against the chance to catch
    # a fish, so that the expected value function is as predicted
    chance = CHANCE_FISH - CHANCE_DIM * depth
    val /= chance

    fishInd = 1 if val/refVal < LESSER_FISH else 0
    fish = LEVELS[index]['fish'][fishInd]

    if random() < chance:
        return catch(fishObj(fish, val))
    elif random() < CHANCE_FAIL:
        return noCatch(fishObj(fish, val))
    elif random() < CHANCE_FAKE:
        return catch(fishObj(FAKE_FISH, 0.0))
    else:
        return catch(fishObj(NO_FISH, 0.0))

# fish object
def fishObj(fish, val):
    actualVal = round(normVal(val, FISH_SD), 0)
    weight = FISH[fish]['weight']
    weight *= actualVal / val if actualVal != 0 else 1
    return {
        'id': fish,
        'name': FISH[fish]['name'],
        'weight': round(weight, 2),
        'value': int(actualVal)
    }

# catch a fish
def catch(fish):
    fish['caught'] = True
    return fish

# fail to catch a fish
def noCatch(fish):
    fish['caught'] = False
    return fish

# return a gaussian with sd expressed in percentage
def normVal(mean, sdp):
    return gauss(mean, mean * sdp)

