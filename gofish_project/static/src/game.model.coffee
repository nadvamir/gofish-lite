# --------------------------------------------------------------
# game module
# --------------------------------------------------------------
# namespace
game = {}

# model of a Fish
class game.Fish
    constructor: (f) ->
        @id     = m.prop new Date().getTime()
        @name   = m.prop f.name
        @value  = m.prop f.value
        @weight = m.prop f.weight

# a player model
class game.Player
    constructor: (p) ->
        @money = m.prop p.money
        @boat  = m.prop p.boat
        @line  = m.prop p.line
        @cue   = m.prop p.cue
        @lineN = m.prop p.lineN
        @cueN  = m.prop p.cueN

# game model
class game.Game
    constructor: (g) ->
        @level        = m.prop g.level
        @day       = m.prop g.day
        @name      = m.prop g.name
        @totalTime = m.prop g.totalTime
        @timeLeft  = m.prop g.timeLeft
        @valCaught = m.prop g.valCaught
        @showDepth = m.prop g.showDepth
        @map       = m.prop g.map
        @position  = m.prop g.position
        @cues      = m.prop g.cues
        @caught    = m.prop []
        for f in g.caught
            @caught().push new game.Fish(f)

game.vm = do ->
    init: ->
        get('/v2/player').then (r) =>
            @player = new game.Player(r.player)

        @info = m.prop ''

        @game = null
        get('/v2/game').then (r) =>
            @game = new game.Game(r.game)

    act: (action) ->
        # don't act during animation
        if game.vm.game.valCaught() == '?'
            return false

        urls =
            fish  : '/action/catchall/1'
            left  : '/action/move/left'
            right : '/action/move/right'

        common = (r) ->
            if r.error
                return m.route '/end'
            g = game.vm.game
            g.timeLeft(g.totalTime() - parseInt(r.time, 10))
            g.cues(r.cues)

        move = (r) ->
            common(r)
            game.vm.game.position(r.position)
            game.vm.info ''

        fish = (r) ->
            # if there is no fishes, then it is the end
            if 0 == r.fishList.length
                return m.route '/end'
            # otherwise, common pattern
            common(r)
            fish = r.fishList[0]
            if null != fish
                g = game.vm.game
                g.valCaught(g.valCaught() + fish.value)
                f = new game.Fish(fish)
                divisor = g.level() == 0 and 1 or 5 * g.level()
                importance = 3 + Math.ceil(f.value() / divisor)
                importance = importance > 140 and 140 or importance
                game.vm.addInfo([
                    'You\'ve caught a ',
                    caught.vm.getItemView.apply(f)
                ], importance)
                g.caught().push f
            else
                game.vm.addInfo 'Nothing was caught', 2

        actions = {fish : fish, left : move, right : move}

        get(urls[action]).then actions[action], -> m.route '/end'

    inGame: ->
        @game != null

    getWaterClass: (i, j) ->
        if i < @game.map()[0][j]
            if j != @game.position() or @game.cues()[i][0] + 1 < 0.001
                'dark-water'
            else
                cue = @game.cues()[i][0]
                cue = 9 if cue > 9
                "light-water.fish-#{cue}"
        else
            'ground'

    # add info text and animate, depending on importance
    addInfo: (text, importance) ->
        @info '.'
        value = @game.valCaught(); @game.valCaught '?'
        maxImp = importance

        end = =>
            @info text
            @game.valCaught value
            true

        timeOutF = =>
            @info ['.' for i in [0..(maxImp-importance)]]
            --importance < 0 and end() or setTimeout timeOutF, 100
            m.redraw()
        setTimeout timeOutF, 100

