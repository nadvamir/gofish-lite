# view
caught.view = -> [
    gTopBar.view(true)
    list.view(game.vm.game.caught().sort(caught.vm.compare), caught.vm.getItemView)
]

