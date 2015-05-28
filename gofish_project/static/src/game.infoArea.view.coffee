# view
infoArea.view = -> m('div#info-area', [
    game.vm.info()
    m('div.right.fa', {
        class: infoArea.cues[game.vm.player.cue() + 1]
        title: game.vm.player.cueN()
    })
    m('div.right.fa', {
        class: infoArea.lines[game.vm.player.line() + 1]
        title: game.vm.player.lineN()
    })
])

