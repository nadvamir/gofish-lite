from random import randint
from random import gauss
from random import random
import gamedef
from yields import *

class YieldMerger:
    generators = {
        'uniform-declining': makeUniformDecliningYield,
        'uniform-constant': makeUniformConstantYield,
        'uniform-random': makeUniformRandomYield,
        'nth-constant': makeNthConstantYield,
        'nth-declining': makeNthDecliningYield,
    }

    # constructor, that tells length of the yields
    def __init__(self, n):
        self.n = n
        self.yields = []

    # a method to add a new yield
    def addYield(self, fishId, fish, depth, player):
        # getting the base yield
        y = self.generators[fish['distribution']['type']](
                self.n, fish['distribution']['options'])

        # base probability to catch fish
        probability = fish['probability']

        # augmenting fish probability based on depth
        depthPenalty = 0.05
        probability -= abs(depth - fish['habitat']) * depthPenalty

        # augmenting fish probability based on player perks
        probability = player.augmentProb(fishId, probability)

        # applying this probability to the existing yield
        y2 = [y[i] * probability for i in range(self.n)]

        # catch the fish if you can and add the resulting yield
        y3 = [self.__catch(y2[i], fish) for i in range(self.n)]
        self.yields.append(y3)

    # returns a merged yield
    def merge(self):
        return [self.__choose(i) for i in range(self.n)]

    # a 'private' method to catch the fish
    def __catch(self, probability, fish):
        if random() <= probability:
            caught = {
                'id': fish['id'],
                'name': fish['name'],
                'weight': round(gauss(fish['weight'],\
                                fish['weight'] * 0.25), 2),
                'length': round(gauss(fish['length'],\
                                fish['length'] * 0.25), 2),
            }
            caught['value'] = round(caught['weight'] / fish['weight'] * fish['value'])
            return caught
        return None

    # a 'private' method to merge one position
    # every caught fish is equally likely to be returned
    def __choose(self, j):
        fish = [self.yields[i][j] for i in range(len(self.yields)) if self.yields[i][j] != None]
        return fish[randint(0, len(fish)-1)] if len(fish) > 0 else None
        
