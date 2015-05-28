# --------------------------------------------------------------
# loading module
# --------------------------------------------------------------
# namespace
loading = {}

# view-model
loading.vm = do ->
    init: -> @loading = m.prop true
    startLoading: -> @loading(true); m.redraw()
    stopLoading: -> @loading(false); m.redraw()

