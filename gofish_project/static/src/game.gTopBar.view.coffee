# Day sub-view
gTopBar.daySW = -> m('.day-ind', [
    'Day '
    m('span', game.vm.game.day())
    '. '
    m('span', game.vm.game.name())
])

# time sub-view
gTopBar.timeSW = -> [
    m('i.fa.fa-clock-o')
    m('span.time-indicator.time-left',
        {style: {width: gTopBar.vm.timeLeftW()+'px'}}, m.trust '&nbsp;')
    m('span.time-indicator.time-full',
        {style: {width: gTopBar.vm.timeFullW()+'px'}}, m.trust '&nbsp;')
]

# money sub-view
gTopBar.moneySW = -> m('div.right.money-ind', [
    '+'
    m('span', {}, gTopBar.vm.valueCaught())
    ' coins'
])

# view
gTopBar.view = (caught) -> m('div.top-bar', [
    gTopBar.timeSW()
    gTopBar.daySW()
    (caught and m('a.right[href=/game]', {config: m.route}, 'Back') or m('a.right[href=/caught]', {config: m.route}, "Caught #{game.vm.game.caught().length} fish"))
    gTopBar.moneySW()
])

