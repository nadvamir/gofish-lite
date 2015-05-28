from django.db import models, connection
from django.db.models import Count
from django.db.models import Avg
from copy import copy
import re

# a data point for charting
class DataPoint(models.Model):
    # players username
    username  = models.TextField()
    # game number for this player
    gameNum   = models.IntegerField()
    # the maximum level player has unlocked
    playerLvl = models.IntegerField()
    # detauls for the cues
    cueDetail = models.IntegerField()
    # game level index
    level     = models.IntegerField()
    # move cost for the player
    moveCost  = models.IntegerField()
    # fishing cost for the player
    fishCost  = models.IntegerField()
    # is this an endgame location
    endGame   = models.IntegerField()
    # how much time did the player spend
    timeSpent = models.IntegerField()
    # how much time was it optimal to spend
    optTime   = models.IntegerField()
    # local optimum for the time
    locOptT   = models.IntegerField()
    # how much money did the player earned
    earnedM   = models.IntegerField()
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
        line = line.split(' ')

        # create a data point
        point = DataPoint(
            username  = line[0],
            gameNum   = int(line[1]),
            playerLvl = int(line[2]),
            cueDetail = int(line[3]),
            level     = int(line[4]),
            moveCost  = int(line[5]),
            fishCost  = int(line[6]),
            endGame   = int(line[7]),
            timeSpent = int(line[8]),
            optTime   = int(line[9]),
            locOptT   = int(line[10]),
            earnedM   = int(line[11]),
            optimalM  = int(line[12]),
            locOptM   = int(line[13]),
            createdAt = int(line[14]))

        # store it
        point.save()

    #############################################################
    # accessors
    #############################################################
    # return all data points for a query
    @staticmethod
    def query(username=None, gameNum=None,
              playerLvl=None, cueDetail=None,
              level=None, moveCost=None, endGame=None):
        qs = DataPoint.objects.all()

        if None != username:  qs = qs.filter(username=username)
        if None != gameNum:   qs = qs.filter(gameNum=gameNum)
        if None != playerLvl: qs = qs.filter(playerLvl=playerLvl)
        if None != cueDetail: qs = qs.filter(cueDetail=cueDetail)
        if None != level:     qs = qs.filter(level=level)
        if None != moveCost:  qs = qs.filter(moveCost=moveCost)
        if None != endGame:   qs = qs.filter(endGame=endGame)

        qs = qs.order_by('id')

        return qs

    # return data for bar chart queries (so, aggregated)
    @staticmethod
    def queryBarData(x):
        xExpr = {
            'optTime'      : '(timeSpent-optTime)',
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
            'optTime'      : '(timeSpent-optTime)',
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
            'usernames'  : qs.values('username').distinct(),
            'gameNums'   : qs.values('gameNum').distinct(),
            'playerLvls' : qs.values('playerLvl').distinct(),
            'cueDetails' : qs.values('cueDetail').distinct(),
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
    # players username
    username  = models.TextField()
    # game number for this player
    gameNum   = models.IntegerField()
    # game level index
    level     = models.IntegerField()
    # details for the cues
    cueDetail = models.IntegerField()
    # line update 
    line      = models.IntegerField()
    # move cost for the player
    moveCost  = models.IntegerField()
    # fishing cost for the player
    fishCost  = models.IntegerField()
    # how many stars have been earned
    stars     = models.IntegerField()
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
        line = line.split(' ')

        # create a data point
        point = EndGame(
            username  = line[0],
            gameNum   = int(line[1]),
            level     = int(line[2]),
            cueDetail = int(line[3]),
            line      = int(line[4]),
            moveCost  = int(line[5]),
            fishCost  = int(line[6]),
            stars     = int(line[7]),
            earnedM   = int(line[8]),
            maxM      = int(line[9]),
            optimalM  = int(line[10]),
            locOptM   = int(line[11]))

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

