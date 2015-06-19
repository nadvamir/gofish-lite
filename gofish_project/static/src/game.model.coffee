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
        @caught = m.prop f.caught

# a player model
class game.Player
    constructor: (p) ->
        @money = m.prop p.money

# game model
class game.Game
    constructor: (g) ->
        @level     = m.prop g.level
        @day       = m.prop g.day
        @name      = m.prop g.name
        @totalTime = m.prop g.totalTime
        @timeLeft  = m.prop g.timeLeft
        @valCaught = m.prop g.valCaught
        @topValue  = m.prop g.topValue
        @position  = m.prop g.position
        @weather   = m.prop g.weather
        @weatherN  = m.prop g.weatherN
        @boat      = m.prop g.boat
        @map       = m.prop g.map
        @caught    = m.prop []
        for f in g.caught
            @caught().push new game.Fish(f) if f.caught

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
                f = new game.Fish(fish)
                importance = 3 + Math.ceil(10 * f.value() / g.topValue())

                if f.caught()
                    g.valCaught(g.valCaught() + fish.value)
                    game.vm.addInfo([
                        'You\'ve caught a ',
                        caught.vm.getItemView.apply(f)
                    ], importance)
                    g.caught().push f
                else
                    game.vm.addInfo([
                        m('span#escape', {
                            onclick: m.trigger('opacity', 0)
                        }, game.vm.getEscapeMsg(f))
                    ], importance, true)
            else
                game.vm.addInfo 'Nothing was caught', 2

        actions = {fish : fish, left : move, right : move}

        get(urls[action]).then actions[action], -> m.route '/end'

    inGame: ->
        @game != null

    getWaterClass: (i, j) ->
        if i < @game.map()[0][j]
            'dark-water'
        else
            'ground'

    getEscapeMsg: (f) ->
        msgs = [[
            caught.vm.getItemView.apply(f)
            m('strong', ' managed to escape!')
        ], [
            caught.vm.getItemView.apply(f)
            m('strong', ' tore the line!')
        ], [
            caught.vm.getItemView.apply(f)
            m('strong', ' got away!')
        ], [
            m('strong', 'You\'ve dropped ')
            caught.vm.getItemView.apply(f)
        ]]
        msgs[Math.floor(Math.random() * msgs.length)]

    # add info text and animate, depending on importance
    addInfo: (text, importance, fade = false) ->
        @info '.'
        value = @game.valCaught(); @game.valCaught '?'
        maxImp = importance

        end = =>
            @info text
            setTimeout ->
                    document.getElementById('escape').click()
                , 500 if fade
            @game.valCaught value
            true

        timeOutF = =>
            @info ['.' for i in [0..(maxImp-importance)]]
            --importance < 0 and end() or setTimeout timeOutF, 100
            m.redraw()
        setTimeout timeOutF, 100

