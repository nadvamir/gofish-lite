# width of the map
MAP_SIZE     = 20
# how much time there is
TOTAL_TIME   = 50
# threshold for moving into secondary fish
LESSER_FISH  = 0.8
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
    'name': 'Cloudy',
    'mult': 3.0
}, {
    'name': 'Rainy',
    'mult': 2.0
}]
LEVELS       = [{
    'name': 'Local Pond',
    'toPlay': 2,
    'boat': 0,
    'fish': ['bass', 'shoe'] # there must always be exactly 2 fish
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

