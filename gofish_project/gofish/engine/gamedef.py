# width of the map
MAP_SIZE     = 20
# how much time there is
TOTAL_TIME   = 50
# threshold for moving into secondary fish
LESSER_FISH  = 0.4
# chance to catch a fish
CHANCE_FISH  = 0.91
# how much chance diminishes per unit of depth
CHANCE_DIM   = 0.04
# chance to fail to catch a fish
CHANCE_FAIL  = 0.7
# chance to catch a fake fish
CHANCE_FAKE  = 0.5
# fake fish id
FAKE_FISH    = 'shoe'
# no fish
NO_FISH      = 'none'
# SD for fish value
FISH_SD      = 0.05
# time spent fishing in each location for all weather conditions
OPT_TIMES    = [
    [4, 8, 12],
    [4, 8, 12],
    [3, 6, 9],
    [2, 4, 6],
    [3, 6, 9]
]
# implied performance (optimality) of players
IMPLIED_PERF = 0.8
# fishing cost is implied 1
BOATS        = [{
    'name': 'Raft',
    'mult': 8.0
}, {
    'name': 'Rowing boat',
    'mult': 4.0
}, {
    'name': 'Motor boat',
    'mult': 2.0
}]

WEATHER      = ['Rainy', 'Cloudy', 'Sunny']

LEVELS       = [{
    'name': 'Local Pond',
    'toPlay': 1,
    'boat': 0,
    'maxdepth': 3,
    'fishVal': 20,
    'fish': ['bream', 'bass'] # there must always be exactly 2 fish
}, {
    'name': 'Lake',
    'toPlay': 3,
    'boat': 0,
    'maxdepth': 5,
    'fishVal': 80,
    'fish': ['pike', 'bream']
}, {
    'name': 'River',
    'toPlay': 3,
    'boat': 1,
    'maxdepth': 7,
    'fishVal': 200,
    'fish': ['catfish', 'salmon']
}, {
    'name': 'Sea',
    'toPlay': 3,
    'boat': 2,
    'maxdepth': 9,
    'fishVal': 800,
    'fish': ['tuna', 'cod']
}, {
    'name': 'Mystery Level',
    'toPlay': 1,
    'boat': 2,
    'maxdepth': 9,
    'fishVal': 2000,
    'fish': ['kraken', 'tuna']
}]

FISH         = {
    'none': {
        'name': 'Nothing',
        'weight': 0.0,
    },
    'bass': {
        'name': 'Bass',
        'weight': 0.2,
    },
    'shoe': {
        'name': 'Shoe',
        'weight': 0.3,
    },
    'pike': {
        'name': 'Pike',
        'weight': 1.5,
    },
    'bream': {
        'name': 'Bream',
        'weight': 1.0,
    },
    'catfish': {
        'name': 'Catfish',
        'weight': 10.0,
    },
    'salmon': {
        'name': 'Salmon',
        'weight': 7.0,
    },
    'tuna': {
        'name': 'Tuna',
        'weight': 20.0,
    },
    'cod': {
        'name': 'Cod',
        'weight': 10.0,
    },
    'kraken': {
        'name': 'Kraken',
        'weight': 10000.0,
    },
}

