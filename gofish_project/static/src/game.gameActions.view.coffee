# view
gameActions.view = -> [
    m('div#game-actions', [
        gameActions.actions().map((action) ->
            m('a[href="#"]', {onclick: link game.vm.act.bind(@, action.action)},
                action.title))])
]

