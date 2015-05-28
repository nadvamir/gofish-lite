from unittest import TestCase
from mock import Mock 
from gofish.engine.gamedef import *
from gofish.models.player import Player

class PlayerTest(TestCase):
    # test moving cost goes inline with gamedef
    def test_getMoveCost(self):
        player = Player.stub()

        # no boats
        self.assertEqual(60, player.getMoveCost())

        # Row Boat
        player.updates['boats'] = 'Row Boat'
        self.assertEqual(40, player.getMoveCost())

        # Motor Boat
        player.updates['boats'] = 'Motor Boat'
        self.assertEqual(20, player.getMoveCost())

        # Speed Boat
        player.updates['boats'] = 'Speed Boat'
        self.assertEqual(10, player.getMoveCost())

    # test cue details
    def test_getCueDetail(self):
        player = Player.stub()

        # no cues
        self.assertEqual(0, player.getCueDetail())

        # A map
        player.updates['cues'] = 'A Map'
        self.assertEqual(1, player.getCueDetail())

        # Old Sonar
        player.updates['cues'] = 'Old Sonar'
        self.assertEqual(3, player.getCueDetail())

        # mermaid
        player.updates['cues'] = 'A Mermaid'
        self.assertEqual(5, player.getCueDetail())

    # test if it returns selected bait
    def test_getSelectedBait(self):
        player = Player.stub()

        # no bait
        self.assertEqual(None, player.getSelectedBait())

        # jig
        player.modifiers['jig'] = True
        self.assertEqual(1.5, player.getSelectedBait()['cod'])

        # worm
        player.modifiers['jig'] = False
        player.modifiers['worm'] = True
        self.assertEqual(1.2, player.getSelectedBait()['bass'])

    # has enough for is really a legacy method, but...
    def test_hasEnoughFor(self):
        player = Player.stub()
        player.money = 10

        self.assertTrue(player.hasEnoughFor(5))
        self.assertTrue(player.hasEnoughFor(10))
        self.assertFalse(player.hasEnoughFor(11))

    # test if probability is properly modified
    def test_augmentProb(self):
        player = Player.stub()

        # by default: no difference
        self.assertEqual(0.5, player.augmentProb('bass', 0.5))

        # line effect
        player.updates['lines'] = 'Strong Line'
        prob = round(player.augmentProb('bass', 0.5), 4)
        self.assertEqual(0.6, prob)

        # + bait effect
        player.modifiers['worm'] = True
        prob = round(player.augmentProb('bass', 0.5), 4)
        self.assertEqual(0.72, prob)

        # - bait effect
        player.modifiers['worm'] = False
        prob = round(player.augmentProb('bass', 0.5), 4)
        self.assertEqual(0.6, prob)

    # test upgrading process
    def test_update(self):
        player = Player.stub()
        player.savePlayer = Mock()
        player.money = 10

        # does not update a non-existant target
        self.assertFalse(player.update('whatever'))

        # does not update if there is not enough money
        self.assertFalse(player.update('lines'))

        # uses up the money and saves the player when successful
        player.money = 3000
        self.assertTrue(player.update('lines'))
        self.assertEqual(2000, player.money)
        player.savePlayer.assert_called_with()

        # does the same second time
        self.assertTrue(player.update('lines'))
        self.assertEqual(0, player.money)
        player.savePlayer.assert_called_with()

        # does not update past the limit
        player.money = 30000000
        self.assertFalse(player.update('lines'))

    # test choosing the bait
    def test_choose(self):
        player = Player.stub()
        player.savePlayer = Mock()
        player.modifiers['jig'] = False
        player.modifiers['worm'] = True

        # it does not select a modifier we don't have
        self.assertFalse(player.choose('wobbler'))

        # it changes the selected modifiers when we have them
        self.assertTrue(player.choose('jig'))
        self.assertTrue(player.modifiers['jig'])
        self.assertFalse(player.modifiers['worm'])
        player.savePlayer.assert_called_with()

    # test buying a bait
    def test_buy(self):
        player = Player.stub()
        player.savePlayer = Mock()
        player.modifiers['worm'] = True
        player.money = 200

        # it does not buy baits that don't exist
        self.assertFalse(player.buy('whatever'))

        # it does not buy baits it already has
        self.assertFalse(player.buy('worm'))

        # it buys baits when everything is ok
        self.assertTrue(player.buy('spinner'))
        self.assertEqual(0, player.money)
        player.savePlayer.assert_called_with()

        # it does not buy baits when there is no money
        self.assertFalse(player.buy('vobbler'))

