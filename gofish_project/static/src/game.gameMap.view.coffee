# a sub view for displaying boat
gameMap.boatSW = -> m('p', {class: game.vm.game.weatherN()}, [
    m('span.boat-' + game.vm.game.boat(), {style:
        {marginLeft: gameMap.TILE_W * game.vm.game.position() + 'px'}})
])

# a sub-view for displaying actual water depth map
gameMap.waterSW = ->
    [m('p', [m('span.' + game.vm.getWaterClass(i, j)) for j in [0...20]]) for i in [0...10]]

# view
gameMap.view = -> m('div#game-map', [
    gameMap.boatSW()
    gameMap.waterSW()
])

