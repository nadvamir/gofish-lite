# sub-view to show single trophy item
trophies.item = (userT, gameT) -> m('li', [
    caught.vm.getItemView.apply(userT)
    m('.right', [
        '/ '
        m('strong', {title: 'High Score'}, gameT.value())
    ])
])

# sub-view to list all trophies
trophies.listTrophies = ->
    if @userT.length > 0
        m('.list', [trophies.item(@userT[i], @gameT[i]) for i in [0...@userT.length]])
    else
        'You have not caught any trophies yet'

# view
trophies.view = -> [
    topBar('Trophies and records:', trophies.vm.player.money())
    m('h2', [
        'Your trophy'
        m('.right', 'Global High Score')
    ])
    trophies.listTrophies.apply(trophies.vm)
]

