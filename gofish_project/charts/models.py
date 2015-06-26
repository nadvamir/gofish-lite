from django.db import models, connection
from django.db.models import Count
from django.db.models import Avg
from copy import copy
import re

# a data point for charting
class DataPoint(models.Model):
    # players user id
    userId    = models.IntegerField()
    # game number for this player
    gameNum   = models.IntegerField()
    # the maximum level player has unlocked
    playerLvl = models.IntegerField()
    # game level index
    level     = models.IntegerField()
    # position
    pos       = models.IntegerField()
    # move cost for the player
    moveCost  = models.IntegerField()
    # is this an endgame location
    endGame   = models.IntegerField()
    # weather conditions
    weather   = models.IntegerField()
    # location depth
    depth     = models.IntegerField()
    # how much time did the player spend
    timeSpent = models.IntegerField()
    # optimal time as designed beforehand
    predOptT  = models.IntegerField()
    # how much time was it optimal to spend
    optTime   = models.IntegerField()
    # local optimum for the time
    locOptT   = models.IntegerField()
    # how much money did the player earned
    earnedM   = models.IntegerField()
    # how much money would pre-designed optimum bring
    predOptM  = models.IntegerField()
    # how much money would optimum bring
    optimalM  = models.IntegerField()
    # how much money would local optimum bring
    locOptM   = models.IntegerField()
    # time the datapoint was recorded
    createdAt = models.IntegerField()

    def __unicode__(self):
        'a data point'

    def toDict(self):
        d = copy(self.__dict__)
        d['_state'] = None
        return d

    #############################################################
    # creators
    #############################################################
    # take a line from log and store it in the database
    @staticmethod
    def insertFromLine(line):
        # our data is space separated
        line = line.split(',')

        # create a data point
        point = DataPoint(
            userId    = int(line[0]),
            gameNum   = int(line[1]),
            playerLvl = int(line[2]),
            level     = int(line[3]),
            pos       = int(line[4]),
            moveCost  = int(line[5]),
            endGame   = int(line[6]),
            weather   = int(line[7]),
            depth     = int(line[8]),
            timeSpent = int(line[9]),
            predOptT  = int(line[10]),
            optTime   = int(line[11]),
            locOptT   = int(line[12]),
            earnedM   = int(line[13]),
            predOptM  = int(line[14]),
            optimalM  = int(line[15]),
            locOptM   = int(line[16]),
            createdAt = int(line[17]))

        # store it
        point.save()

    #############################################################
    # accessors
    #############################################################
    # return all data points for a query
    @staticmethod
    def query(userId=None, gameNum=None, weather=None,
              playerLvl=None, level=None,
              moveCost=None, endGame=None):
        qs = DataPoint.objects.all()

        if None != userId:    qs = qs.filter(userId=userId)
        if None != gameNum:   qs = qs.filter(gameNum=gameNum)
        if None != weather:   qs = qs.filter(weather=weather)
        if None != playerLvl: qs = qs.filter(playerLvl=playerLvl)
        if None != level:     qs = qs.filter(level=level)
        if None != moveCost:  qs = qs.filter(moveCost=moveCost)
        if None != endGame:   qs = qs.filter(endGame=endGame)

        qs = qs.order_by('id')

        return qs

    # return data for bar chart queries (so, aggregated)
    @staticmethod
    def queryBarData(x):
        xExpr = {
            'predOptT'     : '(timeSpent-predOptT)',
            'optTime'      : '(timeSpent-optTime)',
            'predOptM'     : '(earnedM-predOptM)',
            'optMoney'     : '(earnedM-optimalM)',
            'loptTime'     : '(timeSpent-locOptT)',
            'loptMoney'    : '(earnedM-locOptM)',
            'optTimeAbs'   : 'abs(timeSpent-optTime)',
            'optMoneyAbs'  : 'abs(earnedM-optimalM)',
            'loptTimeAbs'  : 'abs(timeSpent-locOptT)',
            'loptMoneyAbs' : 'abs(earnedM-locOptM)'
        }
        x = 'optTime' if x not in xExpr else x

        return DataPoint.objects\
                .extra(select = {'x': xExpr[x]})\
                .values('x')\
                .annotate(Count('id'))\
                .order_by('x')

    # return data for box chart queries (grouped, not aggregated)
    @staticmethod
    def queryBoxData(x, y):
        yExpr = {
            'predOptT'     : '(timeSpent-predOptT)',
            'optTime'      : '(timeSpent-optTime)',
            'predOptM'     : '(earnedM-predOptM)',
            'optMoney'     : '(earnedM-optimalM)',
            'loptTime'     : '(timeSpent-locOptT)',
            'loptMoney'    : '(earnedM-locOptM)',
            'optTimeAbs'   : 'abs(timeSpent-optTime)',
            'optMoneyAbs'  : 'abs(earnedM-optimalM)',
            'loptTimeAbs'  : 'abs(timeSpent-locOptT)',
            'loptMoneyAbs' : 'abs(earnedM-locOptM)'
        }
        x = 'cueDetail' if None == x else x
        y = 'optTimeAbs' if y not in yExpr else y

        return DataPoint.objects\
                .extra(select = {'y': yExpr[y], 'x': x})\
                .values('x', 'y')\
                .order_by(x)

    # return overall info about our data
    @staticmethod
    def describeData():
        qs = DataPoint.objects.all();
        return {
            'userIds'    : qs.values('userId').distinct(),
            'gameNums'   : qs.values('gameNum').distinct(),
            'weathers'   : qs.values('weather').distinct(),
            'playerLvls' : qs.values('playerLvl').distinct(),
            'levels'     : qs.values('level').distinct(),
            'moveCosts'  : qs.values('moveCost').distinct()
        }

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'charts'

# a data point for endgame statistics
class EndGame(models.Model):
    # players user id
    userId    = models.IntegerField()
    # game number for this player
    gameNum   = models.IntegerField()
    # game level index
    level     = models.IntegerField()
    # weather info
    weather   = models.IntegerField()
    # move cost for the player
    moveCost  = models.IntegerField()
    # how much money did the player earned
    earnedM   = models.IntegerField()
    # how much money was it possible to earn
    maxM      = models.IntegerField()
    # how much money would optimum bring
    optimalM  = models.IntegerField()
    # how much money would local optimum bring
    locOptM   = models.IntegerField()

    def __unicode__(self):
        'endgame'

    #############################################################
    # creators
    #############################################################
    # take a line from log and store it in the database
    @staticmethod
    def insertFromLine(line):
        # our data is space separated
        line = line.split(',')

        # create a data point
        point = EndGame(
            userId    = int(line[0]),
            gameNum   = int(line[1]),
            level     = int(line[2]),
            weather   = int(line[3]),
            moveCost  = int(line[4]),
            earnedM   = int(line[5]),
            maxM      = int(line[6]),
            optimalM  = int(line[7]),
            locOptM   = int(line[8]))

        # store it
        point.save()

    #############################################################
    # accessors
    #############################################################
    @staticmethod
    def queryBarData(x, y):
        yExpr = {
            'earned'      : 'avg(earnedM)',
            'diffMax'     : 'avg(earnedM*100/maxM)',
            'diffOpt'     : 'avg(earnedM*100/optimalM)',
            'diffLOpt'    : 'avg(earnedM*100/locOptM)',
        }
        x = re.sub(r'[^a-zA-Z,]', '', x)
        x = 'level' if '' == x else x
        y = 'earned' if y not in yExpr else y

        q = 'SELECT ' + yExpr[y] + ' as y, ' + x + ' FROM charts_endgame WHERE earnedM > 0 GROUP BY ' + x + ' ORDER BY y'
        return connection.cursor().execute(q).fetchall(), x

    @staticmethod
    def queryBoxData(x, y):
        yExpr = {
            'earned'      : '(earnedM)',
            'diffMax'     : '(earnedM*100/maxM)',
            'diffOpt'     : '(earnedM*100/optimalM)',
            'diffLOpt'    : '(earnedM*100/locOptM)',
        }
        x = re.sub(r'[^a-zA-Z,]', '', x)
        x = 'level' if '' == x else x
        y = 'earned' if y not in yExpr else y

        q = 'SELECT ' + yExpr[y] + ' as y, ' + x + ' FROM charts_endgame WHERE earnedM > 0 ORDER BY y'
        return connection.cursor().execute(q).fetchall(), x

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'charts'

