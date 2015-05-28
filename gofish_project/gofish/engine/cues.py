from random import uniform
from random import random
from random import randint

sizeIndicators = [
    0.5, 1.0, 3.0, 10.0
]

#################################################################
# BaseCue
#################################################################
# the base case, no cues are given
class BaseCue(object):
    def get(self):
        return [[-1, 0]]

#################################################################
# DepthCue
#################################################################
# the more complicated case, the depth is revealed
class DepthCue(BaseCue):
    def __init__(self, game, position):
        self.game = game
        self.fish = game.getFishInYield(position)
        self.depth = game.getDephFor(position)

    def get(self):
        cues = []
        for i in range(0, self.depth):
            cues.append(self.aggregateFish(i))
        return cues

    def aggregateFish(self, aggrDepth):
        return [-1, 0]

#################################################################
# FishCue
#################################################################
# in an even more complicated case, the fish information is given
class FishCue(DepthCue):
    def __init__(self, game, position, visibility):
        super(FishCue, self).__init__(game, position)
        self.visibility = visibility

    def aggregateFish(self, aggrDepth):
        # if it is deeper than we see, we have no info:
        if aggrDepth > self.visibility:
            return [-1, 0]

        # calculate average weight and total count of fish here
        # all the fish that is in too shallow places
        # is aggregated at the very bottom
        weight = 0.0
        count = 0.0
        for k, v in self.fish.iteritems():
            if v['depth'] == aggrDepth \
                    or aggrDepth == self.depth - 1 \
                    and v['depth'] > aggrDepth:
                weight += v['weight']
                count += v['count']
        if count > 0:
            weight /= count

        # introducing error with respect to accuracy
        count = self.introduceNoiseToCount(count)
        weight = self.introduceNoiseToWeight(weight)

        # final answer
        return [count, self.getSizeIndicator(weight)]

    def introduceNoiseToCount(self, count):
        # no noise for now
        return count

    def introduceNoiseToWeight(self, weight):
        # no noise for now
        return weight

    # calculating size indicator
    def getSizeIndicator(self, weight):
        i = 0
        while i < len(sizeIndicators) \
                and weight > sizeIndicators[i]:
            i += 1
        return i

#################################################################
# UniformNoiseCue
#################################################################
# finally, we have noisy output
class UniformNoiseCue(FishCue):
    def __init__(self, game, pos, visibility, accuracy):
        super(UniformNoiseCue, self).__init__(game, pos,
                                              visibility)
        self.accuracy = accuracy

    def introduceNoiseToCount(self, count):
        count = round(uniform(count * self.accuracy,
                              count / self.accuracy))
        # ghost sygnals
        if random() > self.accuracy:
            count += randint(0, 2)
        return count

    def introduceNoiseToWeight(self, weight):
        weight = uniform(weight * self.accuracy,
                         weight / self.accuracy)
        # ghost sygnals
        if random() > self.accuracy:
            weight += random()
        return weight

