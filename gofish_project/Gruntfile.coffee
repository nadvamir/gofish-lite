module.exports = (grunt) ->

  fs = require 'fs'
  isModified = (filepath) ->
    now = new Date()
    modified =  fs.statSync(filepath).mtime
    return (now - modified) < 10000

  grunt.initConfig

    coffee:
      options:
        sourceMap: true
        bare: true
        force: true # needs to be added to the plugin
      all:
        expand: true
        cwd: 'static/js/'
        src: 'app.coffee'
        dest: 'static/js'
        ext: '.js'
      modified:
        expand: true
        cwd: 'static/js/'
        src: 'app.coffee'
        dest: 'static/js'
        ext: '.js'
        filter: isModified

    watch:
      coffeescript:
        files: ['static/src/*.coffee']
        tasks: ['concat', 'coffee:modified']

    concat:
        dist:
            src: [
                # common
                'static/src/common.coffee'

                # models
                'static/src/nav.model.coffee'
                'static/src/loading.model.coffee'
                'static/src/home.model.coffee'
                'static/src/game.model.coffee'
                'static/src/game.gTopBar.model.coffee'
                'static/src/game.gameActions.model.coffee'
                'static/src/game.infoArea.model.coffee'
                'static/src/game.gameMap.model.coffee'
                'static/src/caught.model.coffee'
                'static/src/end.model.coffee'
                'static/src/shop.model.coffee'
                'static/src/trophies.model.coffee'

                # controllers
                'static/src/nav.controller.coffee'
                'static/src/loading.controller.coffee'
                'static/src/home.controller.coffee'
                'static/src/game.controller.coffee'
                'static/src/caught.controller.coffee'
                'static/src/end.controller.coffee'
                'static/src/shop.controller.coffee'
                'static/src/trophies.controller.coffee'

                # views
                'static/src/nav.view.coffee'
                'static/src/loading.view.coffee'
                'static/src/home.view.coffee'
                'static/src/game.view.coffee'
                'static/src/game.gTopBar.view.coffee'
                'static/src/game.gameActions.view.coffee'
                'static/src/game.infoArea.view.coffee'
                'static/src/game.gameMap.view.coffee'
                'static/src/caught.view.coffee'
                'static/src/end.view.coffee'
                'static/src/shop.view.coffee'
                'static/src/trophies.view.coffee'

                # main logic
                'static/src/main.coffee'
            ]
            dest: 'static/js/app.coffee'


  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-concat'

  grunt.registerTask 'default', [
      'concat'
      'coffee:all'
      'watch'
  ]

