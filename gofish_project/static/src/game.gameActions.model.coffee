# --------------------------------------------------------------
# game:gameActions module
# --------------------------------------------------------------
# namespace
gameActions = {}

# list of actions available in the game
gameActions.actions = -> [{
        action : 'fish',
        title  : 'fish fast',
        #title  : game.vm.game.position() > 0 and 'move left' or ' return home',
    }, {
        action : 'fish',
        title  : 'fish slow',
    }, {
        action : 'right',
        title  : 'move right',
    }
]


