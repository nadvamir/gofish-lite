# --------------------------------------------------------------
# game:topBar module
# --------------------------------------------------------------
# namespace
gTopBar = {}

# view-model
gTopBar.vm = do ->
    BAR_W = 360

    timeLeftW: ->
        g = game.vm.game
        g.timeLeft() / g.totalTime() * BAR_W

    timeFullW: ->
        BAR_W - @timeLeftW()

    valueCaught: ->
        game.vm.game.valCaught()

