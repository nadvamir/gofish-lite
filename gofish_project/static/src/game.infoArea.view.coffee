# view
infoArea.view = -> m('div#info-area',
    {class: game.vm.game.weatherN()}, [
        game.vm.info()
        m('div.right.fa', {
            class: infoArea.weather[game.vm.game.weather()]
            title: game.vm.game.weatherN()
        })
])

