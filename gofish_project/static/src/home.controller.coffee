# controller
home.controller = ->
    home.vm.init()
    game.vm.init().then ->
        if game.vm.inGame()
            m.route('/game')


