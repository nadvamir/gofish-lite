from unittest import TestCase
from gofish.engine.yields import *
from gofish.engine.yieldmerger import *
from gofish.models.player import Player
from gofish.engine.gamedef import *

class YieldMergerTest(TestCase):
    def test_addYield(self):
        # we can only really test that we add yields
        # with desired fish
        maxTime = TOTAL_TIME / FISHING_COST
        ym = YieldMerger(maxTime)
        # parameter was captured
        self.assertEqual(ym.n, maxTime)

        player = Player.stub()
        yieldC = 0
        # for every level in the game
        for i in range(len(GAME['levels'])):
            for id, fish in getFishForLevel(i).iteritems():
                ym.addYield(id, fish, 5, player)
                yieldC += 1
                # we get one more yield:
                self.assertEqual(len(ym.yields), yieldC)
                # the size of the yield is maxTime
                self.assertEqual(len(ym.yields[yieldC-1]), maxTime)
                # check that this yield only has this fish or nothing
                for y in ym.yields[yieldC-1]:
                    self.assertTrue(None == y or y['id'] == id)

        # for the merge part, we will check that
        # yieldmerger is biased for choosing a fish
        merged = ym.merge()
        self.assertEquals(len(merged), maxTime)
        for i in range(maxTime):
            empty = True
            for y in ym.yields:
                empty = empty and (y[i] == None)
            # none can only be selected if empty
            # otherwise a fish must be there
            self.assertEqual(empty, merged[i] == None)

