# a sub view for displaying boat
gameMap.boatSW = -> m('p', [
    m('span.boat-' + game.vm.player.boat(), {style:
        {marginLeft: gameMap.TILE_W * game.vm.game.position() + 'px'}})
])

# a sub-view for displaying actual water depth map
gameMap.waterSW = ->
    if game.vm.game.showDepth()
        [m('p', [m('span.' + game.vm.getWaterClass(i, j)) for j in [0...20]]) for i in [0...10]]
    else
        [m('span.dark-water') for i in [0...20]]

# view
gameMap.view = -> m('div#game-map', [
    gameMap.boatSW()
    gameMap.waterSW()
])

