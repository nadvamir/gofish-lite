from unittest import TestCase
from django.test import Client

c = Client()

class RegressionTest(TestCase):
    # test getting the list of levels
    def test_levels(self):
        response = c.get('/gofish/api/v2/home/').content
        self.assertTrue('"levels": [{' in response)

    # test getting the player information
    def test_player(self):
        response = c.get('/gofish/api/v2/player/').content
        self.assertTrue('"player":' in response)
        self.assertTrue('"money":' in response)
        self.assertTrue('"lineN":' in response)
        self.assertTrue('"cueN":' in response)
        self.assertTrue('"line":' in response)
        self.assertTrue('"cue":' in response)
        self.assertTrue('"boat":' in response)

    # test trophies call works
    def test_trophies(self):
        response = c.get('/gofish/api/v2/trophies/').content
        self.assertTrue('"gameTrophies": [' in response)
        self.assertTrue('"userTrophies": [' in response)

    # test there is no game until we create one
    def test_game_absence(self):
        response = c.get('/gofish/api/v2/game/').status_code
        self.assertEqual(404, response)

    #############################################################
    # usage scenarios
    #############################################################
    # balanced
    def test_simpleGame(self):
        self.startNewGame()
        [self.catchNext() for i in range(6)]
        self.moveRight(1)
        [self.catchNext() for i in range(6)]
        self.moveRight(2)
        [self.catchNext() for i in range(6)]
        self.moveRight(3)
        [self.catchNext() for i in range(6)]
        self.moveRight(4)
        [self.catchNext() for i in range(6)]
        self.moveRight(5)
        [self.catchNext() for i in range(6)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    # all in one go
    def test_allInOneGame(self):
        self.startNewGame()
        [self.catchNext() for i in range(96)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    # just move
    def test_justMove(self):
        self.startNewGame()
        [self.moveRight(i+1) for i in range(8)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    #############################################################
    # usage scenarios helpers
    #############################################################
    # start new game
    def startNewGame(self):
        newGame = c.get('/gofish/api/start/0/').content
        self.assertTrue('"money"' in newGame)
        self.assertTrue('"caught": []' in newGame)
        self.assertTrue('"cues": 0' in newGame)
        self.assertTrue('"level"' in newGame)
        self.assertTrue('"totalTime"' in newGame)
        self.assertTrue('"map"' in newGame)
        self.assertTrue('"fish"' in newGame)
        self.assertTrue('"timeInLoc"' in newGame)
        self.assertTrue('"yields"' in newGame)
        self.assertTrue('"time"' in newGame)

    # catch the next thing in yield
    def catchNext(self):
        catch = c.get('/gofish/api/action/catchall/1/').content
        self.assertTrue('"fishList"' in catch)
        self.assertTrue('"fishList": []' not in catch)
        self.assertTrue('"cues"' in catch)
        self.assertTrue('"time"' in catch)

    # fail to catch
    def failToCatch(self):
        catch = c.get('/gofish/api/action/catchall/1/').content
        # apparently, we do not fail, just ignore the request
        noCatch = '{"fishList": [], "cues": 0, "time": 480}'
        self.assertEqual(catch, noCatch)

    # move right
    def moveRight(self, newPos):
        move = c.get('/gofish/api/action/move/right/').content
        self.assertTrue('"position": ' + str(newPos) in move)
        self.assertTrue('"cues"' in move)
        self.assertTrue('"time"' in move)

    # fail to move
    def failToMove(self):
        move = c.get('/gofish/api/action/move/right/').content
        self.assertTrue('"error"' in move)

    # ending the game
    def endGame(self):
        end = c.get('/gofish/api/end/').content
        self.assertTrue('"money"' in end)
        self.assertTrue('"avg"' in end)
        self.assertTrue('"maximum"' in end)
        self.assertTrue('"stars"' in end)
        self.assertTrue('"earned"' in end)

