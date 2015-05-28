from unittest import TestCase
from mock import Mock 
from gofish.engine.gamedef import *
from gofish.models.player import Player
from gofish.models.game import *
import gofish.engine.yieldmerger as yieldmerger

class GameTest(TestCase):
    # test retrieval of cues
    def test_getCues(self):
        player = Player.stub()
        game = Game.stub(player, getLevel(0))
        game.level['position'] = 7

        # mock methods
        game.ensureYieldsExist = Mock()
        player.getCueDetail = Mock(return_value=1)

        # patch the generators
        generators[0] = Mock(return_value=0)
        generators[1] = Mock(return_value=1)
        generators[2] = Mock(return_value=2)
        generators[3] = Mock(return_value=3)
        generators[4] = Mock(return_value=4)
        generators[5] = Mock(return_value=5)

        # it makes sure the yield exists
        game.getCues()
        game.ensureYieldsExist.assert_called_with(7)

        # it calls the generator, specific to user
        self.assertEqual(1, game.getCues())
        generators[1].assert_called_with(game, 7)

        # no matter what that user uses
        player.getCueDetail = Mock(return_value=4)
        self.assertEqual(4, game.getCues())
        generators[4].assert_called_with(game, 7)

    # test if the correct depth is returned
    def test_getDepthFor(self):
        game = Game.stub(Player.stub(), getLevel(0))
        depth = game.level['map'][0][7]
        self.assertEqual(depth, game.getDephFor(7))

    # test if the right fish are returned
    def test_getFishInYield(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.level['yields'][7] = [
            {'name': 'Bass', 'weight': 1.0},
            {'name': 'Bass', 'weight': 1.0},
            {'name': 'Bass', 'weight': 1.0},
            {'name': 'Bass', 'weight': 1.0},
            None,
            {'name': 'Bass', 'weight': 2.0},
            {'name': 'Bass', 'weight': 1.0},
        ]

        # when we haven't fished in this location,
        # it returns the aggregation of the whole list
        fish = {'Bass': {
            'weight': 7.0,
            'count': 6,
            'depth': 4,
        }}
        self.assertEqual(fish, game.getFishInYield(7))

        # when we have fished for a while, it returns remainder
        game.level['timeInLoc'][7] = 2
        fish = {'Bass': {
            'weight': 5.0,
            'count': 4,
            'depth': 4,
        }}
        self.assertEqual(fish, game.getFishInYield(7))

    # tests ensuring the yields are present
    def test_ensureYieldsExist(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.setYieldFor = Mock()
        game.saveGame = Mock()

        # if the yield already exists: no action
        game.level['yields'][7] = True
        game.ensureYieldsExist(7)
        self.assertFalse(game.setYieldFor.called)

        # if the yield does not exist and don't save changes
        game.level['yields'][7] = None
        game.ensureYieldsExist(7, False)
        game.setYieldFor.assert_called_with(7)
        self.assertFalse(game.saveGame.called)

        # if the yield does not exist and save changes
        game.ensureYieldsExist(7)
        game.setYieldFor.assert_called_with(7)
        game.saveGame.assert_called_with()

    # test creation of all yields at once
    def test_createAllYields(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.ensureYieldsExist = Mock()
        game.createAllYields()
        self.assertEqual(20, game.ensureYieldsExist.call_count)

    # test recalculation of yields that were already there
    def test_recalcYields(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.setYieldFor = Mock()
        game.level['yields'][0] = True
        game.level['yields'][2] = True
        game.level['yields'][9] = True

        game.recalcYields()
        self.assertEqual(3, game.setYieldFor.call_count)
        game.setYieldFor.assert_any_call(0)
        game.setYieldFor.assert_any_call(2)
        game.setYieldFor.assert_any_call(9)

    # test if optimal time calculations are correct
    def test_getOptimalValue(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.player.getMoveCost = Mock(return_value=10)
        game.ensureYieldsExist = Mock()
        game.level['yields'][7] = [
            {'value': 25.0},
            {'value': 15.0},
            {'value': 15.0},
            {'value': 5.0},
            {'value': 5.0},
            {'value': 50.0},
        ]
        game.level['yields'][0] = game.level['yields'][7]

        # it finds the correct overall optimal time
        self.assertEqual(6, game.getOptimalTime(7))
        game.ensureYieldsExist.assert_called_with(7)

        # it finds the correct local optimal time
        self.assertEqual(3, game.getOptimalTime(7, True))

        # it does not take into account moving cost
        # at the very beginning
        self.assertEqual(1, game.getOptimalTime(0, True))
        self.assertEqual(1, game.getOptimalTime(0))
        game.ensureYieldsExist.assert_called_with(0)

    # test calculation of earnings
    def test_getMoneyEarnedIn(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.level['yields'][7] = [
            {'value': 25.0},
            {'value': 15.0},
            {'value': 15.0},
            {'value': 5.0},
            None,
            {'value': 50.0},
        ]

        self.assertEqual(0.0, game.getMoneyEarnedIn(7, 0))
        self.assertEqual(55.0, game.getMoneyEarnedIn(7, 3))
        self.assertEqual(60.0, game.getMoneyEarnedIn(7, 4))
        self.assertEqual(110.0, game.getMoneyEarnedIn(7, 6))

    # test calculation of endgame optimal earnings
    def test_getOptEarnings(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.getOptimalTime = Mock(return_value=2)
        game.getMoneyEarnedIn = Mock(return_value=1)
        self.assertEqual(7, game.getOptEarnings(5, 60))
        self.assertEqual(7, game.getOptimalTime.call_count)
        game.getMoneyEarnedIn.assert_called_with(6, 2)

    # test if movement code is correct
    def test_move(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.player.getMoveCost = Mock(return_value=10)
        game.logPerformance = Mock()
        game.saveGame = Mock()
        game.getCues = Mock(return_value=42)

        # moving outside from the map returns None
        self.assertEqual(None, game.move('left'))

        # successful move changes game state
        retVal = { 'position': 1, 'cues': 42, 'time': 10 }
        self.assertEqual(retVal, game.move('right'))
        game.saveGame.assert_called_with()
        game.logPerformance.assert_called_with()

        # if there is no more time left, the None is returned
        game.player.getMoveCost = Mock(return_value=10000)
        self.assertEqual(None, game.move('right'))

    # test if inspection returns true results
    def test_inspect(self):
        game = Game.stub(Player.stub(), getLevel(0))
        game.ensureYieldsExist = Mock()
        game.level['yields'][0] = range(96)

        # it returns first 3 elements when asked
        fishList = {'fishList': [0, 1, 2]}
        self.assertEqual(fishList, game.inspect(3))

        # it does not return more than one can possibly fish
        game.level['time'] = 450
        self.assertEqual(None, game.inspect(30))

        # it returns fish elements from the current point
        game.level['timeInLoc'][0] = 1
        fishList = {'fishList': [1, 2, 3]}
        self.assertEqual(fishList, game.inspect(3))

    # test catching non-nil fish
    def test_catchNoNil(self):
        game = Game.stub(Player.stub(), getLevel(0))
        spotYield = [None, 1, 2, None, None, 3, None, None]
        game._common_init = Mock(return_value=(spotYield, 0))
        game._common_catch_init = Mock(return_value=(0, 10, 1))
        game._save_game = Mock()
        game.getCues = Mock(return_value=42)

        # it follows the prescribed logic
        retVal = { 'fishList': [1, 3], 'cues': 42, 'time': 6, }
        self.assertEqual(retVal, game.catchNoNil(['1', '0', '1']))
        game._save_game.assert_called_with([1, 3], 6, 6)

        # it can start from the arbitrary point
        game._common_init = Mock(return_value=(spotYield, 2))
        retVal = { 'fishList': [2, 3], 'cues': 42, 'time': 4, }
        self.assertEqual(retVal, game.catchNoNil(['1', '1']))
        game._save_game.assert_called_with([2, 3], 4, 6)

        # it does not fail when exceeding the limits
        retVal = { 'fishList': [2, 3], 'cues': 42, 'time': 6, }
        self.assertEqual(retVal, game.catchNoNil(['1', '1', '1']))
        game._save_game.assert_called_with([2, 3], 6, 8)

        # it does not fail when the time runs out
        game._common_init = Mock(return_value=(spotYield, 0))
        game._common_catch_init = Mock(return_value=(8, 10, 1))
        retVal = { 'fishList': [1], 'cues': 42, 'time': 10, }
        self.assertEqual(retVal, game.catchNoNil(['1', '1', '1']))
        game._save_game.assert_called_with([1], 10, 2)

    # test catching everything that goes
    def test_catchAll(self):
        game = Game.stub(Player.stub(), getLevel(0))
        spotYield = [None, 1, 2, None, None, 3, None]
        game._common_init = Mock(return_value=(spotYield, 0))
        game._common_catch_init = Mock(return_value=(0, 10, 1))
        game._save_game = Mock()
        game.getCues = Mock(return_value=42)

        # it follows the prescribed logic
        retVal = {
            'fishList': [None, None, 2],
            'cues': 42,
            'time': 3,
        }
        self.assertEqual(retVal, game.catchAll(['1', '0', '1']))
        game._save_game.assert_called_with([2], 3, 3)

        # it can start from the arbitrary point
        game._common_init = Mock(return_value=(spotYield, 1))
        retVal = {
            'fishList': [1, 2],
            'cues': 42,
            'time': 2,
        }
        self.assertEqual(retVal, game.catchAll(['1', '1']))
        game._save_game.assert_called_with([1, 2], 2, 3)

        # it does not fail out of limits
        game._common_init = Mock(return_value=(spotYield, 5))
        game._common_catch_init = Mock(return_value=(4, 10, 1))
        retVal = {
            'fishList': [3, None],
            'cues': 42,
            'time': 6,
        }
        self.assertEqual(retVal, game.catchAll(['1', '0', '1']))
        game._save_game.assert_called_with([3], 6, 7)

        # it does not fail when the time runs out
        game._common_init = Mock(return_value=(spotYield, 0))
        game._common_catch_init = Mock(return_value=(8, 10, 1))
        retVal = {
            'fishList': [None, 1],
            'cues': 42,
            'time': 10,
        }
        self.assertEqual(retVal, game.catchAll(['1', '1', '1']))
        game._save_game.assert_called_with([1], 10, 2)

