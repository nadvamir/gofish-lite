# --------------------------------------------------------------
# main script
# --------------------------------------------------------------
# load up navigation
m.module document.getElementById('nav'), nav

# load up loading overlay
m.module document.getElementById('loading'), loading

# --------------------------------------------------------------
# routing
# --------------------------------------------------------------
m.route.mode = 'hash'
m.route document.getElementById('page'), '/', {
    '/'         : home,
    '/game'     : game,
    '/caught'   : caught,
    '/end'      : end,
    '/trophies' : trophies
}

