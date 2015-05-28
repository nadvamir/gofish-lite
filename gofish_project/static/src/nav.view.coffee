# view
nav.view = (ctrl) -> [
    ctrl.links().map((link) ->
        m('a', {href: link.url, config: m.route}, link.title))
]

