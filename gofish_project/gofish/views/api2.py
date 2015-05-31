from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user
import json

import gofish.models as models
import gofish.engine.gamedef as gamedef
import gofish.engine.level as lvl

#################################################################
# API v2
#################################################################
# get the information about the levels
@allow_lazy_user
def v2home(request):
    player   = models.Player.initialise(request.user)
    response = {'levels': []}

    for i in range(len(gamedef.LEVELS)):
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
            'name'     : gamedef.LEVELS[i]['name'],
            'unlocked' : unlocked,
            'active'   : active,
            'cost'     : lvl.cost(i),
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
        'timeLeft'  : game.level['totalTime'] - game.level['time'],
        'valCaught' : caught,
        'topValue'  : lvl.topValue(game.level['index']),
        'position'  : game.level['position'],
        'caught'    : game.caught,
        'weather'   : game.level['weather'],
        'weatherN'  : gamedef.WEATHER[game.level['weather']]['name'],
        'boat'      : game.level['boat'],
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

