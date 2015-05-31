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
    game = models.Game.initialise(player, int(level))
    response = {'error': 'Could not instantiate game'}
    if None != game:
        response = {} # we don't use this response
    return HttpResponse(json.dumps(response), content_type="application/json")

@allow_lazy_user
def end(request):
    player = models.Player.initialise(request.user)
    game = models.Game.initialise(player)
    response = {'error': 'Game does not exist'}

    if None != game:
        earned, maximum = game.deleteGame()
        stars = player.getAchievement('moneyIn' + str(game.level['index']))
        stars = stars.rating if None != stars else 0
        response = {
            'earned': earned,
            'maximum': maximum,
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
    elif action == 'catchall':
        resp = game.catchAll(par.split(','))
    if None != resp:
        response = resp

    return HttpResponse(json.dumps(response), content_type="application/json")

