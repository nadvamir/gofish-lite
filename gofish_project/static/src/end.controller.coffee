# controller
class end.controller
    constructor: ->
        get('/end').then (r) =>
            @earned  = m.prop r.earned
            @maximum = m.prop r.maximum
            @avg     = m.prop r.avg
            @money   = m.prop r.money
            @stars   = m.prop r.stars

