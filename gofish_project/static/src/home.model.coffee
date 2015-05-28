# --------------------------------------------------------------
# home module
# --------------------------------------------------------------
# namespace
home = {}

# model for game location
class home.Level
    constructor: (lvl) ->
        @id       = m.prop lvl.id
        @name     = m.prop lvl.name
        @unlocked = m.prop lvl.unlocked
        @active   = m.prop lvl.active
        @cost     = m.prop lvl.cost
        @stars    = m.prop lvl.stars
        @highS    = m.prop lvl.highS
        @maxHighS = m.prop lvl.maxHighS

# model for all game locations
home.Levels = Array

home.vm = do ->
    # initialisaton gets the list of levels
    init: ->
        get('/v2/home').then (r) =>
            @levels = new home.Levels()
            for level in r.levels
                @levels.push new home.Level(level)

    chooseLevel: ->
        get('/start/' + @id()).then (r) ->
            if r.error
                console.log r
            else
                m.route('/game')

    # an item view function, has to be bound to a model
    getItemView: ->
        # unlocked and playable
        if @unlocked()
            [
                m('a[href=#]', {onclick:
                    link home.vm.chooseLevel.bind(@)}, @name())
                ', unlocked. '
                m('span', {title: 'Your Performance'}, [
                    ['*' for star in [0...@stars()]]
                ])
                # high score
                m('.right', [
                    m('strong', {title: 'Your High Score'}, @highS())
                    ' / '
                    m('strong', {title: 'High Score'}, @maxHighS())
                ])
            ]
        # available to unlock
        else if @active() and @cost() <= game.vm.player.money()
            [
                m('a[href=#]', {onclick:
                    link home.vm.chooseLevel.bind(@)}, @name())
                ', cost '
                m('strong', {title: 'Cost in coins'}, @cost())
            ]
        # not available to unlock
        else if @active()
            [
                @name()
                ', cost '
                m('strong', {title: 'Cost in coins'}, @cost())
            ]
        # not yet playable
        else
            @name()

