from django.db import models
from django.contrib.auth.models import User
import json
import logging
import time
from fractions import gcd

from player import Player
import gofish.engine.gamedef as gamedef
import gofish.engine.level as lvl

# a game class, representing the current level and everything
# that happens in it
class Game(models.Model):
    player = models.OneToOneField(Player)
    # a json representation of the current level
    level  = models.TextField(default='{}')
    # a json representation of the fish caught
    caught = models.TextField(default='[]')
    
    #############################################################
    # access
    #############################################################
    # a method to get initialised game object
    @staticmethod
    def initialise(player, index=None):
        game = None

        # try to find existing game
        try:
            game = Game.objects.get(player=player)
        # if there is none, create a new one
        except Game.DoesNotExist:
            # if we did not specify level, this means
            # that we don't want to create a game
            if None == index:
                return None

            # if it is the first time we play, 
            # then consume the money
            if player.level < index:
                # can only move one level at a time
                if index - player.level > 1:
                    return None
                # if there is not enough money, return None
                cost = lvl.cost(index)
                if player.money < cost:
                    return None
                # remove the price of the level from player
                player.money -= cost
                player.level += 1

            # update the number of games for this player
            player.numGames += 1
            # save changes to player
            player.savePlayer()

            game = Game(player=player,
                        level=json.dumps(lvl.get(index)))
            game.save()

        # unmarshal json fields
        game.unmarshal()
        # error if the game is restored, and it is different
        # than the one we ask for
        if None != index and game.level['index'] != index:
            # or, maybe end the previous game and start a new one
            return None

        return game

    # a method to get test game
    @staticmethod
    def stub(player, level):
        game = Game(player=player, level=json.dumps(level))
        game.unmarshal()
        return game

    # a special delete method, that calculates the value
    # of the fish caught, and rewards the player
    def deleteGame(self):
        # log the players performance for the research
        # (counting end game in the same fashion, as move)
        self.logPerformance(True)

        # calculate, how much was earned
        earned = 0
        for fish in self.caught:
            if fish['caught']:
                earned += fish['value']
                # also, store it if it is a trophy
                self.player.storeAchievement(fish['id'],
                                             fish['weight'],
                                             fish['value'])

        # log endgame performance
        # overall statistics
        maximum = self.logEndGame(earned)

        # give stars
        # 70 % of maximum performance = 1 star
        # 85 % of maximum performance = 2 stars
        # 95 % of maximum performance = 3 stars
        rating = 0
        ratings = [maximum * 0.5, maximum * 0.75, maximum * 0.9]
        while rating < len(ratings) and earned > ratings[rating]:
            rating += 1

        self.player.storeAchievement('moneyIn' +\
                str(self.level['index']), earned, rating)

        # store the money 
        self.player.money += earned
        self.player.allMoney += earned
        self.player.maxMoney += maximum
        self.player.savePlayer()

        self.delete()
        return earned, maximum

    # a method to marshal fields
    def marshal(self):
        if not isinstance(self.level, basestring):
            self.level = json.dumps(self.level)
        if not isinstance(self.caught, basestring):
            self.caught = json.dumps(self.caught)

    # a method to unmarshal fields
    def unmarshal(self):
        if isinstance(self.level, basestring):
            self.level = json.loads(self.level)
        if isinstance(self.caught, basestring):
            self.caught = json.loads(self.caught)

    # a special save method, to ensure, that we
    # serialise our fields
    def saveGame(self):
        self.marshal()
        self.save()
        self.unmarshal()
    
    def __unicode__(self):
        return ','.join(map(str, [
            self.player, self.level['index']
        ]))

    #############################################################
    # regular logging with helpers
    #############################################################
    # a method to log users performance
    def logPerformance(self, endGame = False):
        logger = logging.getLogger('gofish')

        levelInfo   = self
        weather     = int(
                gamedef.WEATHER[self.level['weather']]['mult'])
        pos         = self.level['position']
        timeSpent   = self.level['timeInLoc'][pos]
        optimalTime = self.getOptimalTime(pos)
        localOptT   = self.getOptimalTime(pos, local=True)
        moneyEarned = int(self.getMoneyEarnedIn(pos, timeSpent))
        optimalM    = int(self.getMoneyEarnedIn(pos, optimalTime))
        localOptM   = int(self.getMoneyEarnedIn(pos, localOptT))
        endGame     = '1' if endGame else '0'
        moveCost    = int(lvl.moveC(self.level['index']))
        createdAt   = int(time.time())

        msg = [
            levelInfo, moveCost, endGame, weather,
            timeSpent, optimalTime, localOptT,
            moneyEarned, optimalM, localOptM,
            createdAt
        ]

        logger.info(','.join(map(str, msg)))

    # returns optimal time to spend in the given location
    def getOptimalTime(self, pos, local = False):
        maxVal = 0.0; val = 0.0; bestTime = 0; time = 1

        boatMCost = lvl.moveC(self.level['index'])
        travelCost = boatMCost if pos > 0 else 0

        for fish in self.level['yields'][pos]:
            if fish['caught']:
                val += fish['value']
            vRatio = val / (time + travelCost)
            if vRatio > maxVal:
                maxVal = vRatio
                bestTime = time
            elif vRatio < maxVal and True == local:
                # local optima found
                return bestTime
            time += 1

        return bestTime

    # returns how much money was earned in loc till given time
    def getMoneyEarnedIn(self, pos, timeSpent):
        return sum([fish['value'] for fish in self.level['yields'][pos][0:timeSpent] if fish['caught']])

    #############################################################
    # endgame logging with helpers
    #############################################################
    # a method to log at endgame
    # tries to evaluate earned vs maximum earned in the game
    def logEndGame(self, earned):
        logger = logging.getLogger('endgame')

        # rest
        gameNr    = self.player.numGames
        player    = self.player.user.id
        level     = self.level['index']
        weather   = int(
                gamedef.WEATHER[self.level['weather']]['mult'])
        moveCost  = int(lvl.moveC(self.level['index']))
        maxEarn   = int(self.getMaxEarnings(moveCost))
        optEarn   = self.getOptEarnings(moveCost)
        lOptEarn  = self.getOptEarnings(moveCost, local=True)

        msg = [
            player, gameNr, level, weather,
            moveCost, int(earned),
            maxEarn, optEarn, lOptEarn
        ]

        logger.info(','.join(map(str, msg)))
        return maxEarn

    # a method that returns maximum possible earnings
    def getMaxEarnings(self, moveCost):
        y = self.level['yields']
        # maximum depth of movement (num moves)
        maxDepth = gamedef.TOTAL_TIME
        # optimisation: use less memory by lowering time
        t = gamedef.TOTAL_TIME
        moveC = int(lvl.moveC(self.level['index']))

        # array of best values
        values = [[0 for i in range(maxDepth + 1)] for j in range(len(y))]

        # and now let's calculate benefits
        for pos in range(len(y)):
            # first element for every yield will stay 0,
            # as it means we did not fish there
            nfish = len(y[pos]) - pos * moveC
            nfish = 0 if nfish < 0 else nfish
            for i in range(nfish):
                val = y[pos][i]['value'] if y[pos][i]['caught'] else 0
                values[pos][i+1] = values[pos][i] + val

        # perform a O(n*t*k^2) algorithm :(
        val, moves = opt(values, t, moveC)
        return val

    # a method that returns earnings based on optimal strategy
    def getOptEarnings(self, moveCost, local=False):
        time = gamedef.TOTAL_TIME + moveCost
        money = 0

        for pos in range(len(self.level['yields'])):
            time -= moveCost
            if time <= 0:
                return money

            optimalTime = self.getOptimalTime(pos, local)
            if optimalTime > time:
                optimalTime = time
            money += int(self.getMoneyEarnedIn(pos, optimalTime))
            time -= optimalTime

        return money

    #############################################################
    # actions
    #############################################################
    # a method to move player on the map
    def move(self, direction):
        size = gamedef.MAP_SIZE
        position = self.level['position']
        cost = lvl.moveC(self.level['index'])

        step = -1
        if direction == 'right':
            step = 1

        position += step
        if position < 0 or position >= size:
            return None

        if self.level['time'] + cost > self.level['totalTime']:
            return None

        # log the players performance for the research
        self.logPerformance()

        self.level['position'] = position
        self.level['time'] += cost
        self.saveGame()
        return {
            'position': position,
            'time': self.level['time'],
        }

    # a method to actually catch the next N fish or nothings
    # fishList is an array of '1' and '0' telling
    # if we managed to forage the given yield
    def catchAll(self, fishList):
        spotYield, timeInSpot = self._common_init()
        time, totalTime, fCost = self._common_catch_init()

        caught = [] # caught does not have Nones
        response = []
        for succeeded in fishList:
            if time + fCost > totalTime or timeInSpot == len(spotYield):
                break

            if '1' == succeeded and \
                    spotYield[timeInSpot]['id'] != gamedef.NO_FISH:
                caught.append(spotYield[timeInSpot])
                response.append(spotYield[timeInSpot])
            else:
                response.append(None)

            time += fCost
            timeInSpot += 1

        self._save_game(caught, time, timeInSpot)

        return {
            'fishList': response,
            'time': time
        }

    # a helper method to get common variables
    def _common_init(self):
        pos = self.level['position']
        spotYield = self.level['yields'][pos]
        timeInSpot = self.level['timeInLoc'][pos]

        return spotYield, timeInSpot

    # a helper method to get variables common across catch calls
    def _common_catch_init(self):
        time = self.level['time']
        totalTime = self.level['totalTime']
        fCost = 1

        return time, totalTime, fCost

    # a helper method to save common endstate
    def _save_game(self, caught, time, timeInSpot):
        self.caught += caught
        self.level['time'] = time
        self.level['timeInLoc'][self.level['position']] = timeInSpot
        self.saveGame()

    ##############################################################
    # Django boilerplate
    ##############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

##############################################################
# internal helper functions
##############################################################
# returns an array copy with updated index
def insert(choices, pos, val):
    a = choices[:]
    a[pos] = val
    return a

# calculates cost of choices, + value
def costAndValue(choices, values, moveC):
    fished = False
    time = 0
    value = 0
    for i in xrange(len(choices)-1, -1, -1):
        if 0 != choices[i]:
            fished = True
            time += moveC + choices[i]
            value += values[i][choices[i]]
        elif fished:
            time += moveC
    # we have added 1 too many moving cost
    time -= moveC
    return time, value

# find maximum attainable value
def opt(values, time, moveC):
    # 'weights', times in our case
    w = [(0, [0 for j in range(len(values))]) for i in range(time+1)]

    # for all positions
    for pos in range(len(values)):
        # optimisation: don't look at fish that are uncacheable
        nfish = len(values[pos]) - pos * moveC
        nfish = 0 if nfish < 0 else nfish
        # for all overall earnings in the position
        for i in range(nfish):
            # for all possible points in time
            for j in range(len(w)):
                # optimisation: non-increasing values will never
                # be optimal
                if values[pos][i] == values[pos][i-1]:
                    continue
                # optimisation: skip most of 0 value w's
                if j > 0 and 0 == w[j][0]:
                    continue
                # try to make this move from that point in time
                choices = insert(w[j][1], pos, i)
                t, v = costAndValue(choices, values, moveC)
                if t <= time:
                    # store the maximum value so far for that time
                    if w[t][0] < v:
                        w[t] = (v, choices)

    return w[time]

