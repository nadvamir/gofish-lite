from gamedef import *
from random import gauss
from random import randint
from math import exp

# cost of unlocking given level
def cost(index):
    if 0 == index:
        return 0
    times = LEVELS[index-1]['toPlay']
    # times to play x optimal earnings for each weather group
    optE = sum([optEarnings(index, i) for i in range(0, len(WEATHER))])
    return int(IMPLIED_PERF * times * optE)

# a level object
def get(index):
    weather = randint(0, len(WEATHER)-1)
    return {
        'index': index,
        'name': LEVELS[index]['name'],
        'boat': LEVELS[index]['boat'],
        'weather': weather,
        'position': 0,
        'time': 0,
        'totalTime': TOTAL_TIME,
        'timeInLoc': [0 for i in range(0, MAP_SIZE)],
        'yields': getYields(index, weather)
    }

# move cost in this level
def moveC(index):
    return BOATS[LEVELS[index]['boat']]['mult']

# optimal earnings in an average game
def optEarnings(index, weather):
    vf = valueF(index, weather)
    w = WEATHER[weather]['mult']
    b = moveC(index)
    optT = w * b - b
    optE = sum([vf(i) for i in range(1, int(optT)+1)])
    return int(optE * TOTAL_TIME / optT) # a very rough estimate

# fish value function for a game with given parameters
def valueF(index, weather):
    w = WEATHER[weather]['mult']
    b = moveC(index)
    v = topValue(index)
    return lambda x: v * exp(-x / b / (w-1))

# top value for a fish
def topValue(index):
    return INIT_VAL + BASE_VAL ^ index

# generate all yields
def getYields(index, weather):
    return [genYield(index, weather) for i in range(0, MAP_SIZE)]

# generate a yield
def genYield(index, weather):
    vf = valueF(index, weather)
    return [getFish(index, vf, i) for i in range(1, TOTAL_TIME+1)]

# get a particular fish
def getFish(index, vf, i):
    refVal = vf(1)
    val = vf(i)

    fishInd = 1 if val/refVal < LESSER_FISH else 0
    fish = LEVELS[index]['fish'][fishInd]

    actualVal = round(normVal(val, FISH_SD), 0)
    return {
        'id': fish,
        'name': FISH[fish]['name'],
        'weight': round(FISH[fish]['weight'] * actualVal / val, 2),
        'value': int(actualVal)
    }

# return a gaussian with sd expressed in percentage
def normVal(mean, sdp):
    return gauss(mean, mean * sdp)

