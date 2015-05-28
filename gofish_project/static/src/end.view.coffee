# view
end.view = (c) -> [
    m('div.top-bar.large', [
        'This day is over!'
    ])
    m('ul.list', [
        m('li', [
            'Earned '
            m('strong', c.earned())
            ' coins out of '
            m('strong', c.maximum())
            ' possible in this go.'
        ])
        m('li', [
            'Now you have '
            m('strong', c.money())
            ' coins.'
        ])
    ])
]

