from unittest import TestCase
from mock import Mock 
from gofish.engine.cues import *
from gofish.engine.gamedef import *
from gofish.models.player import Player
from gofish.models.game import Game

class BaseCueTest(TestCase):
    def test_get(self):
        # base cue always returns same thing
        self.assertEquals(BaseCue().get(), [[-1, 0]])

class DepthCueTest(TestCase):
    def test_get(self):
        player = Player.stub()
        # for every level
        for i in range(len(GAME['levels'])):
            game = Game.stub(player, getLevel(i))
            # for every position it shows no info
            for j in range(len(game.level['map'][0])):
                game.setYieldFor(j) # creating a yield
                depth = game.getDephFor(j)
                output = [[-1, 0]] * depth
                self.assertEquals(output, DepthCue(game, j).get())

class FishCueTest(TestCase):
    def test_get(self):
        # mocking the game object
        game = Mock()
        game.getFishInYield = Mock(return_value={
            'test': {
                'depth': 4, # 0-indexed
                'count': 3,
                'weight': 2.0,
            }
        })
        game.getDephFor = Mock(return_value=9)

        ########################################################
        # scenario 1: max visibility
        ########################################################
        cue = FishCue(game, 7, 10)
        # called our mock methods
        game.getFishInYield.assert_called_with(7)
        game.getDephFor.assert_called_with(7)
        # the result has shown our fish
        output = [[0.0, 0]] * 4 + [[3.0, 1]] + [[0.0, 0]] * 4
        self.assertEqual(output, cue.get())

        ########################################################
        # scenario 2: limited visibility
        ########################################################
        cue = FishCue(game, 7, 4)
        # the result has shown our fish and hidden stuff
        output = [[0.0, 0]] * 4 + [[3.0, 1]] + [[-1, 0]] * 4
        self.assertEqual(output, cue.get())

        ########################################################
        # scenario 3: fish invisible
        ########################################################
        cue = FishCue(game, 7, 1)
        # the result did not show our fish
        output = [[0.0, 0]] * 2 + [[-1, 0]] * 7
        self.assertEqual(output, cue.get())

        ########################################################
        # scenario 4: fish very large
        ########################################################
        game.getFishInYield = Mock(return_value={
            'test': {
                'depth': 4, # 0-indexed
                'count': 3,
                'weight': 31.0,
            }
        })
        cue = FishCue(game, 7, 10)
        # the result has shown our large fish
        output = [[0.0, 0]] * 4 + [[3.0, 4]] + [[0.0, 0]] * 4
        self.assertEqual(output, cue.get())

        ########################################################
        # scenario 5: depth less than preferred
        ########################################################
        game.getDephFor = Mock(return_value=2)
        cue = FishCue(game, 7, 10)
        # we see our fish on the bottom
        output = [[0.0, 0], [3.0, 4]]
        self.assertEqual(output, cue.get())

class UniformNoiseCueTest(TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.getFishInYield = Mock(return_value={})
        self.game.getDephFor = Mock(return_value=9)

    # checking that random noise is within range for count
    def test_introduceNoiseToCount(self):
        # 50 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 0.5)
        for i in range(100):
            count = cue.introduceNoiseToCount(10)
            self.assertTrue(count >= 5)
            self.assertTrue(count <= 22) # up to 2 ghosts

        # 75 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 0.75)
        for i in range(100):
            count = cue.introduceNoiseToCount(10)
            self.assertTrue(count >= 7.5)
            self.assertTrue(count <= 15.4)

        # 100 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 1.0)
        for i in range(100):
            count = cue.introduceNoiseToCount(10)
            self.assertEquals(count, 10.0)

    # checking that random noise is within range for weight
    def test_introduceNoiseToCount(self):
        # 50 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 0.5)
        for i in range(100):
            count = cue.introduceNoiseToWeight(10)
            self.assertTrue(count >= 5)
            self.assertTrue(count <= 21) # up to +1 ghost kg

        # 75 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 0.75)
        for i in range(100):
            count = cue.introduceNoiseToWeight(10)
            self.assertTrue(count >= 7.5)
            self.assertTrue(count <= 14.4)

        # 100 % accuracy
        cue = UniformNoiseCue(self.game, 7, 10, 1.0)
        for i in range(100):
            count = cue.introduceNoiseToWeight(10)
            self.assertEquals(count, 10.0)

