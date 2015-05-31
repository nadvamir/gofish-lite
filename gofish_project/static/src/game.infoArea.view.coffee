# view
infoArea.view = -> m('div#info-area', [
    game.vm.info()
    m('div.right.fa', {
        class: infoArea.weather[game.vm.game.weather()]
        title: game.vm.game.weatherN()
    })
])

