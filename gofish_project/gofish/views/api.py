from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user
import json

import gofish.models as models
import gofish.engine.gamedef as gamedef

#################################################################
# API
#################################################################
@allow_lazy_user
def start(request, level):
    player = models.Player.initialise(request.user)
    game = models.Game.initialise(player,
                                  gamedef.getLevel(int(level)))
    response = {'error': 'Could not instantiate game'}
    if None != game:
        response = {
            'level': game.level,
            'cues': game.getCues(),
            'caught': game.caught,
            'money': player.money,
        }
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def end(request):
    player = models.Player.initialise(request.user)
    game = models.Game.initialise(player)
    response = {'error': 'Game does not exist'}

    if None != game:
        earned, maximum, avg = game.deleteGame()
        stars = player.getAchievement('moneyIn' + str(game.level['index']))
        stars = stars.rating if None != stars else 0
        response = {
            'earned': earned,
            'maximum': maximum,
            'avg': avg,
            # the game had a different player object
            # which were not linked.
            # at this point the database is updated
            # but this player does not reflect updates.
            # I wonder how many more bugs like that
            # are in the code...
            'money': player.money + earned,
            'stars': stars
        }

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def action(request, action, par):
    player = models.Player.initialise(request.user)
    game = models.Game.initialise(player)
    response = {'error': 'Could not perform the action'}
    if None == game:
        return HttpResponse(json.dumps(response), content_type="application/json")

    resp = None
    if action == 'move':
        resp = game.move(par)
    elif action == 'inspect':
        resp = game.inspect(int(par))
    elif action == 'catchnonil':
        resp = game.catchNoNil(par.split(','))
    elif action == 'catchall':
        resp = game.catchAll(par.split(','))
    if None != resp:
        response = resp

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def update(request, target):
    player = models.Player.initialise(request.user)

    response = {'error': 'Could not update the thing'}
    if player.update(target):
        response = {'player': player.toDict()}

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def choose(request, modifier):
    player = models.Player.initialise(request.user)

    response = {'error': 'Could not buy the bait'}
    if player.choose(modifier):
        response = {'player': player.toDict()}

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def buy(request, modifier):
    player = models.Player.initialise(request.user)

    response = {'error': 'Could not buy the bait'}
    if player.buy(modifier):
        response = {'player': player.toDict()}

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getgame(request):
    player = models.Player.initialise(request.user)
    response = gamedef.GAME
    response['player'] = player.toDict()

    # add star scores
    for i in range(len(response['levels'])):
        stars = player.getAchievement('moneyIn' + str(i))
        stars = stars.rating if None != stars else 0
        response['levels'][i]['stars'] = stars

    # add trophies
    response['trophies'] = {}
    for fish in response['fish'].keys():
        trophy = player.getAchievement(fish)
        trophy = trophy.toDict() if None != trophy else {'value': 0.0, 'rating': 0}
        response['trophies'][fish] = trophy

    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getmodifiers(request):
    response = gamedef.GAME['modifiers']
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def getupdates(request):
    response = gamedef.GAME['updates']
    return HttpResponse(json.dumps(response), content_type="application/json")

