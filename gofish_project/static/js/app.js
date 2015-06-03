var caught, end, gTopBar, game, gameActions, gameMap, get, home, infoArea, link, list, loading, nav, topBar, trophies, url;

list = {};

list.view = function(items, view) {
  if (items.length > 0) {
    return m('ul.list', [
      items.map(function(item) {
        return m('li', {
          key: item.id()
        }, [view.apply(item)]);
      })
    ]);
  } else {
    return m('ul.list', [m('li', [m('span', 'Nothing to show yet')])]);
  }
};

topBar = function(text, money) {
  return m('div.top-bar', [
    m('span.large', text), m('div.right.money-ind', [
      m('span', {
        title: 'Your money'
      }, money), ' coins'
    ])
  ]);
};

link = function(f) {
  return function(e) {
    e.preventDefault();
    return f();
  };
};

url = function(specifics) {
  return '/gofish/api' + specifics;
};

get = function(q) {
  loading.vm.startLoading();
  return m.request({
    method: 'GET',
    url: url(q)
  }).then(function(response) {
    loading.vm.stopLoading();
    return response;
  });
};

nav = {};

nav.LinkList = function() {
  return m.prop([
    {
      url: '/',
      title: 'Game'
    }, {
      url: '/trophies',
      title: 'Troph.'
    }
  ]);
};

loading = {};

loading.vm = (function() {
  return {
    init: function() {
      return this.loading = m.prop(true);
    },
    startLoading: function() {
      this.loading(true);
      return m.redraw();
    },
    stopLoading: function() {
      this.loading(false);
      return m.redraw();
    }
  };
})();

home = {};

home.Level = (function() {
  function Level(lvl) {
    this.id = m.prop(lvl.id);
    this.name = m.prop(lvl.name);
    this.unlocked = m.prop(lvl.unlocked);
    this.active = m.prop(lvl.active);
    this.cost = m.prop(lvl.cost);
    this.stars = m.prop(lvl.stars);
    this.highS = m.prop(lvl.highS);
    this.maxHighS = m.prop(lvl.maxHighS);
  }

  return Level;

})();

home.Levels = Array;

home.vm = (function() {
  return {
    init: function() {
      return get('/v2/home').then((function(_this) {
        return function(r) {
          var level, _i, _len, _ref;
          _this.levels = new home.Levels();
          _ref = r.levels;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            level = _ref[_i];
            _this.levels.push(new home.Level(level));
          }
          return _this.perf = m.prop(r.perf);
        };
      })(this));
    },
    chooseLevel: function() {
      return get('/start/' + this.id()).then(function(r) {
        if (r.error) {
          return console.log(r);
        } else {
          return m.route('/game');
        }
      });
    },
    getItemView: function() {
      var star;
      if (this.unlocked()) {
        return [
          m('a[href=#]', {
            onclick: link(home.vm.chooseLevel.bind(this))
          }, this.name()), ', unlocked. ', m('span', {
            title: 'Your Performance'
          }, [
            [
              (function() {
                var _i, _ref, _results;
                _results = [];
                for (star = _i = 0, _ref = this.stars(); 0 <= _ref ? _i < _ref : _i > _ref; star = 0 <= _ref ? ++_i : --_i) {
                  _results.push('*');
                }
                return _results;
              }).call(this)
            ]
          ]), m('.right', [
            m('strong', {
              title: 'Your High Score'
            }, this.highS()), ' / ', m('strong', {
              title: 'High Score'
            }, this.maxHighS())
          ])
        ];
      } else if (this.active() && this.cost() <= game.vm.player.money()) {
        return [
          m('a[href=#]', {
            onclick: link(home.vm.chooseLevel.bind(this))
          }, this.name()), ', cost ', m('strong', {
            title: 'Cost in coins'
          }, this.cost())
        ];
      } else if (this.active()) {
        return [
          this.name(), ', cost ', m('strong', {
            title: 'Cost in coins'
          }, this.cost())
        ];
      } else {
        return this.name();
      }
    }
  };
})();

game = {};

game.Fish = (function() {
  function Fish(f) {
    this.id = m.prop(new Date().getTime());
    this.name = m.prop(f.name);
    this.value = m.prop(f.value);
    this.weight = m.prop(f.weight);
    this.caught = m.prop(f.caught);
  }

  return Fish;

})();

game.Player = (function() {
  function Player(p) {
    this.money = m.prop(p.money);
  }

  return Player;

})();

game.Game = (function() {
  function Game(g) {
    var f, _i, _len, _ref;
    this.level = m.prop(g.level);
    this.day = m.prop(g.day);
    this.name = m.prop(g.name);
    this.totalTime = m.prop(g.totalTime);
    this.timeLeft = m.prop(g.timeLeft);
    this.valCaught = m.prop(g.valCaught);
    this.topValue = m.prop(g.topValue);
    this.position = m.prop(g.position);
    this.weather = m.prop(g.weather);
    this.weatherN = m.prop(g.weatherN);
    this.boat = m.prop(g.boat);
    this.caught = m.prop([]);
    _ref = g.caught;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      f = _ref[_i];
      if (f.caught) {
        this.caught().push(new game.Fish(f));
      }
    }
  }

  return Game;

})();

game.vm = (function() {
  return {
    init: function() {
      get('/v2/player').then((function(_this) {
        return function(r) {
          return _this.player = new game.Player(r.player);
        };
      })(this));
      this.info = m.prop('');
      this.game = null;
      return get('/v2/game').then((function(_this) {
        return function(r) {
          return _this.game = new game.Game(r.game);
        };
      })(this));
    },
    act: function(action) {
      var actions, common, fish, move, urls;
      if (game.vm.game.valCaught() === '?') {
        return false;
      }
      urls = {
        fish: '/action/catchall/1',
        left: '/action/move/left',
        right: '/action/move/right'
      };
      common = function(r) {
        var g;
        if (r.error) {
          return m.route('/end');
        }
        g = game.vm.game;
        return g.timeLeft(g.totalTime() - parseInt(r.time, 10));
      };
      move = function(r) {
        common(r);
        game.vm.game.position(r.position);
        return game.vm.info('');
      };
      fish = function(r) {
        var f, g, importance;
        if (0 === r.fishList.length) {
          return m.route('/end');
        }
        common(r);
        fish = r.fishList[0];
        if (null !== fish) {
          g = game.vm.game;
          f = new game.Fish(fish);
          importance = 3 + Math.ceil(10 * f.value() / g.topValue());
          if (f.caught()) {
            g.valCaught(g.valCaught() + fish.value);
            game.vm.addInfo(['You\'ve caught a ', caught.vm.getItemView.apply(f)], importance);
            return g.caught().push(f);
          } else {
            return game.vm.addInfo([m('span.warning', [caught.vm.getItemView.apply(f), ' managed to ', m('strong', 'escape!')])], importance);
          }
        } else {
          return game.vm.addInfo('Nothing was caught', 2);
        }
      };
      actions = {
        fish: fish,
        left: move,
        right: move
      };
      return get(urls[action]).then(actions[action], function() {
        return m.route('/end');
      });
    },
    inGame: function() {
      return this.game !== null;
    },
    getWaterClass: function(i, j) {
      return 'dark-water';
    },
    addInfo: function(text, importance) {
      var end, maxImp, timeOutF, value;
      this.info('.');
      value = this.game.valCaught();
      this.game.valCaught('?');
      maxImp = importance;
      end = (function(_this) {
        return function() {
          _this.info(text);
          _this.game.valCaught(value);
          return true;
        };
      })(this);
      timeOutF = (function(_this) {
        return function() {
          var i;
          _this.info([
            (function() {
              var _i, _ref, _results;
              _results = [];
              for (i = _i = 0, _ref = maxImp - importance; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
                _results.push('.');
              }
              return _results;
            })()
          ]);
          --importance < 0 && end() || setTimeout(timeOutF, 100);
          return m.redraw();
        };
      })(this);
      return setTimeout(timeOutF, 100);
    }
  };
})();

gTopBar = {};

gTopBar.vm = (function() {
  var BAR_W;
  BAR_W = 360;
  return {
    timeLeftW: function() {
      var g;
      g = game.vm.game;
      return g.timeLeft() / g.totalTime() * BAR_W;
    },
    timeFullW: function() {
      return BAR_W - this.timeLeftW();
    },
    valueCaught: function() {
      return game.vm.game.valCaught();
    }
  };
})();

gameActions = {};

gameActions.actions = function() {
  return [
    {
      action: 'left',
      title: game.vm.game.position() > 0 && 'move left' || ' return home'
    }, {
      action: 'fish',
      title: 'fish here'
    }, {
      action: 'right',
      title: 'move right'
    }
  ];
};

infoArea = {};

infoArea.weather = ['fa-sun-o', 'fa-cloud', 'fa-sellsy'];

gameMap = {};

gameMap.TILE_W = 40;

caught = {};

caught.vm = (function() {
  return {
    getItemView: function() {
      return [
        m('div.fish-img', {
          "class": this.name()
        }), m('span', this.name()), ', weight ', this.weight(), ' kg, value ', m('strong', {
          title: 'Coins you\'ve earned'
        }, this.value())
      ];
    },
    compare: function(a, b) {
      return b.value() - a.value();
    }
  };
})();

end = {};

trophies = {};

trophies.Trophies = Array;

trophies.vm = (function() {
  return {
    init: function() {
      get('/v2/player').then((function(_this) {
        return function(r) {
          return _this.player = new game.Player(r.player);
        };
      })(this));
      this.userT = new trophies.Trophies();
      this.gameT = new trophies.Trophies();
      return get('/v2/trophies').then((function(_this) {
        return function(r) {
          var i, t, _i, _len, _ref;
          _ref = r.userTrophies;
          for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
            t = _ref[i];
            if (t.value > 0) {
              _this.userT.push(new game.Fish(t));
              _this.gameT.push(new game.Fish(r.gameTrophies[i]));
            }
          }
          _this.userT.sort(function(a, b) {
            return a.name() > b.name();
          });
          return _this.gameT.sort(function(a, b) {
            return a.name() > b.name();
          });
        };
      })(this));
    }
  };
})();

nav.controller = function() {
  return {
    links: nav.LinkList()
  };
};

loading.controller = (function() {
  function controller() {
    loading.vm.init();
  }

  return controller;

})();

home.controller = function() {
  home.vm.init();
  return game.vm.init().then(function() {
    if (game.vm.inGame()) {
      return m.route('/game');
    }
  });
};

game.controller = (function() {
  function controller() {
    game.vm.init();
  }

  return controller;

})();

caught.controller = function() {
  return game.vm.init();
};

end.controller = (function() {
  function controller() {
    get('/end').then((function(_this) {
      return function(r) {
        _this.earned = m.prop(r.earned);
        _this.maximum = m.prop(r.maximum);
        _this.money = m.prop(r.money);
        return _this.stars = m.prop(r.stars);
      };
    })(this));
  }

  return controller;

})();

trophies.controller = function() {
  return trophies.vm.init();
};

nav.view = function(ctrl) {
  return [
    ctrl.links().map(function(link) {
      return m('a', {
        href: link.url,
        config: m.route
      }, link.title);
    })
  ];
};

loading.view = function(ctrl) {
  return loading.vm.loading() && m('div', [m('span.fa.fa-spin.fa-spinner', ' '), ' Loading...']) || '';
};

home.view = function() {
  return [topBar('Choose a location:', game.vm.player.money()), m('h2', ['Performance', m('.right', home.vm.perf() + '%')]), m('h2', ['Location', m('.right', 'High Score')]), list.view(home.vm.levels, home.vm.getItemView)];
};

game.view = function(ctrl) {
  return [gTopBar.view(), gameActions.view(), infoArea.view(), gameMap.view()];
};

gTopBar.daySW = function() {
  return m('.day-ind', ['Day ', m('span', game.vm.game.day()), '. ', m('span', game.vm.game.name())]);
};

gTopBar.timeSW = function() {
  return [
    m('i.fa.fa-clock-o'), m('span.time-indicator.time-left', {
      style: {
        width: gTopBar.vm.timeLeftW() + 'px'
      }
    }, m.trust('&nbsp;')), m('span.time-indicator.time-full', {
      style: {
        width: gTopBar.vm.timeFullW() + 'px'
      }
    }, m.trust('&nbsp;'))
  ];
};

gTopBar.moneySW = function() {
  return m('div.right.money-ind', ['+', m('span', {}, gTopBar.vm.valueCaught()), ' coins']);
};

gTopBar.view = function(caught) {
  return m('div.top-bar', [
    gTopBar.timeSW(), gTopBar.daySW(), caught && m('a.right[href=/game]', {
      config: m.route
    }, 'Back') || m('a.right[href=/caught]', {
      config: m.route
    }, "Caught " + (game.vm.game.caught().length) + " fish"), gTopBar.moneySW()
  ]);
};

gameActions.view = function() {
  return [
    m('div#game-actions', [
      gameActions.actions().map(function(action) {
        return m('a[href="#"]', {
          onclick: link(game.vm.act.bind(this, action.action))
        }, action.title);
      })
    ])
  ];
};

infoArea.view = function() {
  return m('div#info-area', {
    "class": game.vm.game.weatherN()
  }, [
    game.vm.info(), m('div.right.fa', {
      "class": infoArea.weather[game.vm.game.weather()],
      title: game.vm.game.weatherN()
    })
  ]);
};

gameMap.boatSW = function() {
  return m('p', {
    "class": game.vm.game.weatherN()
  }, [
    m('span.boat-' + game.vm.game.boat(), {
      style: {
        marginLeft: gameMap.TILE_W * game.vm.game.position() + 'px'
      }
    })
  ]);
};

gameMap.waterSW = function() {
  var i, j;
  return [
    (function() {
      var _i, _results;
      _results = [];
      for (i = _i = 0; _i < 10; i = ++_i) {
        _results.push(m('p', [
          (function() {
            var _j, _results1;
            _results1 = [];
            for (j = _j = 0; _j < 20; j = ++_j) {
              _results1.push(m('span.' + game.vm.getWaterClass(i, j)));
            }
            return _results1;
          })()
        ]));
      }
      return _results;
    })()
  ];
};

gameMap.view = function() {
  return m('div#game-map', [gameMap.boatSW(), gameMap.waterSW()]);
};

caught.view = function() {
  return [gTopBar.view(true), list.view(game.vm.game.caught().sort(caught.vm.compare), caught.vm.getItemView)];
};

end.view = function(c) {
  return [m('div.top-bar.large', ['This day is over!']), m('ul.list', [m('li', ['Earned ', m('strong', c.earned()), ' coins out of ', m('strong', c.maximum()), ' possible in this go.']), m('li', ['Now you have ', m('strong', c.money()), ' coins.'])])];
};

trophies.item = function(userT, gameT) {
  return m('li', [
    caught.vm.getItemView.apply(userT), m('.right', [
      '/ ', m('strong', {
        title: 'High Score'
      }, gameT.value())
    ])
  ]);
};

trophies.listTrophies = function() {
  var i;
  if (this.userT.length > 0) {
    return m('.list', [
      (function() {
        var _i, _ref, _results;
        _results = [];
        for (i = _i = 0, _ref = this.userT.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
          _results.push(trophies.item(this.userT[i], this.gameT[i]));
        }
        return _results;
      }).call(this)
    ]);
  } else {
    return 'You have not caught any trophies yet';
  }
};

trophies.view = function() {
  return [topBar('Trophies and records:', trophies.vm.player.money()), m('h2', ['Your trophy', m('.right', 'Global High Score')]), trophies.listTrophies.apply(trophies.vm)];
};

m.module(document.getElementById('nav'), nav);

m.module(document.getElementById('loading'), loading);

m.route.mode = 'hash';

m.route(document.getElementById('page'), '/', {
  '/': home,
  '/game': game,
  '/caught': caught,
  '/end': end,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
