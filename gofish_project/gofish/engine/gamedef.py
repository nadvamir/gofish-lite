# here we have a GAME definition object, already priced
TOTAL_TIME   = 96
# fishing cost is implied 1
# optimal fishing time is theoretically BOAT x WEATHER
# but in reality they seem to just correlate strongly
BOAT         = [{
    'name': 'Raft',
    'mult': 4.0
}, {
    'name': 'Rowing boat',
    'mult': 2.0
}, {
    'name': 'Motor boat',
    'mult': 1.0
}]
WEATHER      = [{
    'name': 'Sunny',
    'mult': 4.0
}, {
    'name': 'Windy',
    'mult': 3.0
}, {
    'name': 'Rainy',
    'mult': 2.0
}]
LEVELS       = [{
    'name': 'Local Pond',
    'toPlay': 3,
    'boat': 0,
    'fish': ['bass', 'shoe']
}, {
    'name': 'Lake',
    'toPlay': 5,
    'boat': 0,
    'fish': ['pike', 'bream']
}, {
    'name': 'River',
    'toPlay': 5,
    'boat': 1,
    'fish': ['catfish', 'salmon']
}, {
    'name': 'Sea',
    'toPlay': 5,
    'boat': 2,
    'fish': ['tuna', 'cod']
}]

FISH         = {
    'bass': {
        'id': 'bass',
        'name': 'Bass',
        'weight': 0.2,
    },
    'shoe': {
        'id': 'shoe',
        'name': 'Shoe',
        'weight': 0.3,
    },
    'pike': {
        'id': 'pike',
        'name': 'Pike',
        'weight': 1.5,
    },
    'bream': {
        'id': 'bream',
        'name': 'Bream',
        'weight': 1.0,
    },
    'catfish': {
        'id': 'catfish',
        'name': 'Catfish',
        'weight': 10.0,
    },
    'salmon': {
        'id': 'salmon',
        'name': 'Salmon',
        'weight': 7.0,
    },
    'tuna': {
        'id': 'tuna',
        'name': 'Tuna',
        'weight': 20.0,
    },
    'cod': {
        'id': 'cod',
        'name': 'Cod',
        'weight': 10.0,
    },
}

# a function to get the fish for this level
def getFishForLevel(level):
    f = {}
    for fish, locF in GAME['levels'][level]['fish'].iteritems():
        newFish = dict(GAME['fish'][fish])
        newFish['probability'] = locF['probability']
        newFish['distribution'] = locF['distribution']
        f[fish] = newFish
    return f

# a function to get the level dict
def getLevel(level):
    lvl = dict(GAME['levels'][level])
    lvl['index'] = level
    lvl['time'] = 0
    lvl['totalTime'] = TOTAL_TIME
    lvl['map'] = maps.generate(maxDepth=(lvl['maxDepth'] + 1), width=20)
    lvl['position'] = 0

    # time spent in each location
    lvl['timeInLoc'] = [0 for i in range(20)]

    # yields are not yet defined
    lvl['yields'] = [None for i in range(20)]

    return lvl

# a function to get index for an update
def getIndex(name, update):
    for i in range(0, len(GAME['updates'][update])):
        if GAME['updates'][update][i]['name'] == name:
            return i
    return -1

