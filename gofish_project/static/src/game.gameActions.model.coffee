# --------------------------------------------------------------
# game:gameActions module
# --------------------------------------------------------------
# namespace
gameActions = {}

# list of actions available in the game
gameActions.actions = -> [{
        action : 'left',
        title  : game.vm.game.position() > 0 and 'move left' or ' return home',
    }, {
        action : 'fish',
        title  : 'fish here',
    }, {
        action : 'right',
        title  : 'move right',
    }
]


