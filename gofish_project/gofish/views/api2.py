from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user
import json

import gofish.models as models
import gofish.engine.gamedef as gamedef

#################################################################
# API v2
#################################################################
# get the information about the levels
@allow_lazy_user
def v2home(request):
    player   = models.Player.initialise(request.user)
    response = {'levels': []}

    for i in range(len(gamedef.GAME['levels'])):
        # star scores for player
        record = player.getAchievement('moneyIn' + str(i))
        stars = record.rating if None != record else 0
        highS = record.value if None != record else 0
        # highest scores for everyone
        records = models.Achievement.getTop('moneyIn' + str(i))
        maxHighS = records[0].value if 0 != len(records) else 0
        # other parameters
        unlocked = player.level >= i
        active = player.level + 1 >= i
        # putting it all together
        response['levels'].append({
            'id'       : i,
            'name'     : gamedef.GAME['levels'][i]['name'],
            'unlocked' : unlocked,
            'active'   : active,
            'cost'     : gamedef.GAME['levels'][i]['cost'],
            'stars'    : stars,
            'highS'    : highS,
            'maxHighS' : maxHighS,
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the information about the player
@allow_lazy_user
def v2player(request):
    player   = models.Player.initialise(request.user)
    response = {'player': {
        'money' : player.money,
        'boat'  : getIndex(player, 'boats'),
        'line'  : getIndex(player, 'lines'),
        'cue'   : getIndex(player, 'cues'),
        'lineN' : getName(player, 'lines'),
        'cueN'  : getName(player, 'cues')
    }}
    return HttpResponse(json.dumps(response), content_type="application/json")

# get the information about the active game
@allow_lazy_user
def v2game(request):
    player = models.Player.initialise(request.user)
    game   = models.Game.initialise(player)
    if None == game:
        return HttpResponseNotFound()

    caught = reduce(lambda a, f: a + f['value'], game.caught, 0)
    response = {'game' : {
        'level'     : game.level['index'],
        'day'       : player.numGames,
        'name'      : game.level['name'],
        'totalTime' : game.level['totalTime'],
        'timeLeft'  : game.level['totalTime']-game.level['time'],
        'valCaught' : caught,
        'showDepth' : 'cues' in player.updates,
        'map'       : game.level['map'],
        'position'  : game.level['position'],
        'cues'      : game.getCues(),
        'caught'    : game.caught,
    }}

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the trophies
@allow_lazy_user
def v2trophies(request):
    player = models.Player.initialise(request.user)
    response = {'userTrophies': [], 'gameTrophies': []}

    for _, fish in gamedef.GAME['fish'].iteritems():
        # add user trophies
        trophy = player.getAchievement(fish['id'])
        trophy = trophy.toDict() if None != trophy else {'value': 0.0, 'rating': 0}
        response['userTrophies'].append({
            'name'   : fish['name'],
            'value'  : trophy['rating'],
            'weight' : trophy['value'],
        })

        # add best overall trophies
        trophy = models.Achievement.getTop(fish['id'])
        trophy = trophy[0].toDict() if 0 != len(trophy) else {'value': 0.0, 'rating': 0}
        response['gameTrophies'].append({
            'name'   : fish['name'],
            'value'  : trophy['rating'],
            'weight' : trophy['value'],
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

# get the shop items
@allow_lazy_user
def v2shop(request):
    response = {
        'boats' : [],
        'lines' : [],
        'cues'  : []
    }

    # add a default boat
    response['boats'].append({
        'name' : 'Raft',
        'cost' : 0,
        'perk' : 'It floats.'
    })
    # add a default line
    response['lines'].append({
        'name' : 'Old Fishing Line',
        'cost' : 0,
        'perk' : 'Found in the attic.'
    })
    # add a default queue
    response['cues'].append({
        'name' : 'Your Eyes',
        'cost' : 0,
        'perk' : 'You can\'t quite see underwater...'
    })

    # build boats
    lastSpeed = gamedef.MOVE_COST
    lastName = 'Raft'
    for boat in gamedef.GAME['updates']['boats']:
        response['boats'].append({
            'name' : boat['name'],
            'cost' : boat['price'],
            'perk' : '<span>' + str(round(
                (gamedef.MOVE_COST + boat['time']) \
                / 1.0 / lastSpeed * 100)) + \
                '%</span> faster than a ' + lastName
        })
        lastSpeed = gamedef.MOVE_COST + boat['time']
        lastName = boat['name']

    # build lines
    for line in gamedef.GAME['updates']['lines']:
        response['lines'].append({
            'name' : line['name'],
            'cost' : line['price'],
            'perk' : '<span>' + \
                    str(line['probability'] * 100 - 100) + \
                    '%</span> more fish!'
        })

    # build cues
    cues = gamedef.GAME['updates']['cues']
    response['cues'].append({
        'name' : cues[0]['name'],
        'cost' : cues[0]['price'],
        'perk' : 'It shows you how deep water is'
    })
    for i in range(1, len(cues)):
        response['cues'].append({
            'name' : cues[i]['name'],
            'cost' : cues[i]['price'],
            'perk' : 'It shows fish up to <span>' + \
                    str(cues[i]['depth']) + \
                    '</span> tiles below you with a <span>' + \
                    str(cues[i]['accuracy']) + \
                    '%</span> accuracy'
        })

    return HttpResponse(json.dumps(response), content_type="application/json")

################################################################
# Helpers
################################################################
# get index for a player update
def getIndex(player, update):
    return -1 if update not in player.updates else gamedef.getIndex(player.updates[update], update)

# get the name of a player's update
def getName(player, update):
    return player.updates.get(update, '')

