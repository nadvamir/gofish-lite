import gofish.engine.gamedef as gamedef
import gofish.models as models
from math import sqrt

# moving costs
MOV_C = [60, 60, 40, 20, 20]

# a simulator, that calculates average yields
# for every game level
class YieldSimulation(object):
    ############################################################
    # Public API
    ############################################################
    # run the simulation, producing non-reduced data
    def __init__(self, N=100):
        self.N = N
        self.yields = []
        player = models.Player.stub()

        for i in range(len(gamedef.GAME['levels'])):
            level = gamedef.getLevel(i)
            self.yields.append(self.simulate(player, level))

    # return yields for every level
    # that are expressed as fish per fishing time in loc
    def getYields(self):
        # reduce helper function to accumulate fish
        # caught in different simulations simulations
        def addUp(acc, instance):
            # for every time spent in fishing in this instance
            for t in range(len(instance)):
                for fish, amount in instance[t].iteritems():
                    acc[t][fish] += amount / self.N
            return acc

        # getting initial yield without creating level object
        def insert0(d, k): d[k] = 0.0; return d
        init = lambda i: map(lambda y: reduce(insert0, y.keys(), {}), i)
        # averaging all simulation yields for the level
        averageLvl = lambda lvlYield: reduce(addUp, lvlYield, init(lvlYield[0]))

        return map(lambda l: averageLvl(l), self.yields)

    # describe yields in terms of money
    def describeYields(self, fishVal):
        lvl = [-1]
        def incrLvl(): lvl[0] += 1; return lvl[0]
        toMoney = lambda l, ind: map(lambda i: \
                YieldSimulation.getOptYield(fishVal, i, \
                                            MOV_C[ind]), l)

        def describe(level):
            mean     = getMean(level)
            variance = getVariance(level, mean)
            return mean, sqrt(variance)

        return map(lambda l: describe(toMoney(l, incrLvl())), self.yields)

    # export simulation earnings distribution to file
    def exportEarnings(self, fish):
        with open('earnings.csv', 'w') as fw:
            # for every level
            for lvl in range(len(self.yields)):
                earnings = [YieldSimulation.getOptYield(fish, y, MOV_C[lvl]) for y in self.yields[lvl]]
                fw.write(','.join(map(lambda x: str(x), earnings)) + "\n")

    # export fish distributions per level
    @staticmethod
    def exportDistributions(yields, fish):
        # value in the location timespot
        def val(t):
            y = 0.0
            for f, n in t.iteritems():
                y += fish[f] * n
            return y

        with open('distributions.csv', 'w') as fw:
            # for every level
            for lvl in range(len(yields)):
                value = [val(t) for t in yields[lvl]]
                fw.write(','.join(map(lambda x: str(x), value)) + "\n")


    # calculating optimal yield
    # lvlYield has average fish values earned fishing up to
    # this time
    @staticmethod
    def getOptYield(fish, lvlYield, movingCost=gamedef.MOVE_COST):
        # for now, static parameters:
        time = 480.0
        fishingCost = gamedef.FISHING_COST

        # optimal yield is that, which maximises
        # the overall yield of the game
        maxYield = 0.0
        # for every time we fish in a location
        for i in range(len(lvlYield)):
            y = 0.0
            # yield from this location
            for f, n in lvlYield[i].iteritems():
                y += fish[f] * n
            # yield overall from a game
            y *= time / ((i + 1) * fishingCost + movingCost)
            # saving the largest so far:
            if maxYield < y:
                maxYield = y

        return maxYield

    ############################################################
    # MonteCarlo internals
    ############################################################
    # run a simulation
    def simulate(self, player, level):
        return [self.getYield(player, level) for n in range(self.N)]

    # get an average yield of a level
    def getYield(self, player, level):
        # create a game stub
        game = models.Game.stub(player, level)

        # set yields for every position
        nPos = len(game.level['yields'])
        for i in range(nPos):
            game.setYieldFor(i)

        # aggregate the yield
        nTimes, y = getInitY(level)
        for i in range(nPos):
            for j in range(nTimes):
                if None != game.level['yields'][i][j]:
                    # we divide by nPos, because the yield is
                    # aggregated over all the positions into
                    # single value
                    y[j][game.level['yields'][i][j]['id']] += \
                            1.0 / nPos

        # withing the yield, accumulate the value
        for i in range(1, nTimes):
            for fish in y[i].keys():
                y[i][fish] += y[i-1][fish]

        return y

#################################################################
# Private Functions
#################################################################
# a function to convert a list of fish to yield
def toYield(l):
    y = {}
    for fish in l.keys():
        y[fish] = 0.0
    return y

# get initial yield for the level
def getInitY(level):
    nTimes = gamedef.TOTAL_TIME / gamedef.FISHING_COST
    y = [toYield(gamedef.getFishForLevel(level['index'])) \
            for i in range(nTimes)]
    return nTimes, y

# returns mean for an array
def getMean(X):
    return reduce(lambda x, y: x + y, X, 0.0) / len(X)

# returns variance of an array
def getVariance(X, mean):
    return reduce(lambda x, y: x + pow(y - mean, 2), X, 0.0) / len(X)

