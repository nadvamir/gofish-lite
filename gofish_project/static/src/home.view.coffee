# view
home.view = -> [
    topBar('Choose a location:', game.vm.player.money())
    m('h2', [
        'Performance'
        m('.right', home.vm.perf() + '%')
    ])
    m('h2', [
        'Location'
        m('.right', 'High Score')
    ])
    list.view(home.vm.levels, home.vm.getItemView)
]

