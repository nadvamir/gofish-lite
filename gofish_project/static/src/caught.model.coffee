# --------------------------------------------------------------
# caught module
# --------------------------------------------------------------
# namespace
caught = {}

# view-model
caught.vm = do ->
    getItemView: -> [
        m('div.fish-img', {class: @name()})
        m('span', @name())
        ', weight '
        @weight()
        ' kg, value '
        m('strong', {title: 'Coins you\'ve earned'}, @value())
    ]
    compare: (a, b) ->
        b.value() - a.value()

