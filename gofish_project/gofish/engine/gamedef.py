# width of the map
MAP_SIZE     = 20
# how much time there is
TOTAL_TIME   = 50
# threshold for moving into secondary fish
LESSER_FISH  = 0.7
# chance to catch a fish
CHANCE_FISH  = 0.5
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
# initial value of a fish
INIT_VAL     = 20
# base value for a level
BASE_VAL     = 10
# implied performance (optimality) of players
IMPLIED_PERF = 1.0
# fishing cost is implied 1
# optimal fishing time is theoretically BOAT x WEATHER
# but in reality they seem to just correlate strongly
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
WEATHER      = [{
    'name': 'Sunny',
    'mult': 5.0
}, {
    'name': 'Cloudy',
    'mult': 3.5
}, {
    'name': 'Rainy',
    'mult': 2.5
}]
LEVELS       = [{
    'name': 'Local Pond',
    'toPlay': 2,
    'boat': 0,
    'fish': ['bream', 'bass'] # there must always be exactly 2 fish
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
}

