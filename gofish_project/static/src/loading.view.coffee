# view
loading.view = (ctrl) ->
    (loading.vm.loading() and m('div', [
        m('span.fa.fa-spin.fa-spinner', ' ')
        ' Loading...'
    ]) or '')

