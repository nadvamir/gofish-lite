# --------------------------------------------------------------
# game:gameActions module
# --------------------------------------------------------------
# namespace
gameActions = {}

# list of actions available in the game
gameActions.actions = -> [{
        action : 'fish',
        title  : 'fish (1 min)',
    }, {
        action : 'right',
        title  : "move right (#{game.vm.game.moveC()} min)",
    }
]


