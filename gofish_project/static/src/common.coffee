#= require <loading.model.coffee>
# --------------------------------------------------------------
# reusable components and functions
# --------------------------------------------------------------
# list component, produces a list when given an array of items
list = {}
list.view = (items, view) ->
    if items.length > 0
        m('ul.list', [
            items.map((item) ->
                m('li', {key: item.id()}, [view.apply(item)]))
        ])
    else
        m('ul.list', [m('li', [
            m('span', 'Nothing to show yet')
        ])])

# gets a top bar with a message and money from a player
topBar = (text, money) -> m('div.top-bar', [
    m('span.large', text)
    m('div.right.money-ind', [
        m('span', {title: 'Your money'}, money)
        ' coins'
    ])
])

# returns an onclick for links that runs js instead of defaults
link = (f) ->
    (e) ->
        e.preventDefault()
        f()

# returns an url that works with server
url = (specifics) -> '/gofish/api' + specifics

# makes a get query
get = (q) ->
    loading.vm.startLoading()
    m.request(method: 'GET', url: url(q)).then (response) ->
        loading.vm.stopLoading()
        response


