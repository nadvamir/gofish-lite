from django.db import models
from django.contrib.auth.models import User
import json
import gofish.engine.gamedef as gamedef
from achievement import Achievement

# a player of the game
class Player(models.Model):
    user      = models.OneToOneField(User)

    # how much currency this player has
    money     = models.IntegerField(default=10)
    # how many games has he played in total
    numGames  = models.IntegerField(default=0)
    # what is the highest level unlocked by a player
    level     = models.IntegerField(default=0)

    #############################################################
    # access
    #############################################################
    # a method to get initialised player object
    @staticmethod
    def initialise(user):
        player = None

        # try to find existing player
        try:
            player = Player.objects.get(user=user)
        # if there is none, create a new one
        except Player.DoesNotExist:
            player = Player(user=user)
            player.save()

        return player

    # a method to get test user
    @staticmethod
    def stub():
        player = Player(user=User())
        return player

    # a special save method, to ensure, that we
    # serialise our fields
    def savePlayer(self):
        self.save()

    def toDict(self):
        return {
            'money'     : self.money,
            'level'     : self.level,
        }

    def __unicode__(self):
        return self.user.username + ' ' \
                + str(self.numGames) + ' ' \
                + str(self.level) + ' ' \
                + str(self.getCueDetail())

    #############################################################
    # helpers
    #############################################################
    # returns movement cost of this player
    def getMoveCost(self):
        cost = gamedef.MOVE_COST
        return cost

    # returns the level of detail of cues
    def getCueDetail(self):
        if 'cues' not in self.updates:
            return 0

        upds = gamedef.GAME['updates']
        for v in upds['cues']:
            if self.updates['cues'] == v['name']:
                return v['cueDetail']

    # return a bait that the player has selected
    def getSelectedBait(self):
        for bait in self.modifiers.iterkeys():
            if self.modifiers[bait]:
                return gamedef.GAME['modifiers'][bait]
        return None

    # returns if there is enough money to buy something
    def hasEnoughFor(self, amount):
        return self.money >= amount

    # augment probability to catch a fiven fish
    def augmentProb(self, fish, probability):
        # fist of all, special items
        upds = gamedef.GAME['updates']
        for key in self.updates:
            for v in upds[key]:
                if self.updates[key] == v['name'] and 'probability' in v:
                    # FIXME: do I really want +10%
                    # instead of 10% increase?
                    probability += v['probability'] - 1

        # then check if the bait has any effect
        bait = self.getSelectedBait()
        if bait and fish in bait:
            probability *= bait[fish]

        return probability

    # return a specific achievement
    def getAchievement(self, name):
        try:
            return Achievement.objects.get(player=self, name=name)
        except Achievement.DoesNotExist:
            return None

    # a method to store achievements
    def storeAchievement(self, name, value=0.0, rating=0):
        Achievement.upsert(self, name, value, rating)

    #############################################################
    # actions
    #############################################################
    # tries to update a given target
    def update(self, target):
        if target in gamedef.GAME['updates']:
            # find the next update
            upds = gamedef.GAME['updates'][target]
            update = upds[0]
            if target in self.updates:
                for i in range(len(upds)):
                    if upds[i]['name'] == self.updates[target]:
                        if i < len(upds) - 1:
                            update = upds[i+1]
                            break
                        else:
                            return False
            # buy it
            if self.hasEnoughFor(update['price']):
                self.money -= update['price']
                self.updates[target] = update['name']
                self.savePlayer()
                return True
        return False

    # tries to select a given bait
    def choose(self, bait):
        # bait doesn't exist
        if bait not in self.modifiers:
            return False

        # unselect all baits
        for k in self.modifiers.iterkeys():
            self.modifiers[k] = False

        # select bait
        self.modifiers[bait] = True
        self.savePlayer()

        return True

    # tries to buy a given bait
    def buy(self, bait):
        # bait doesn't exist
        if bait not in gamedef.GAME['modifiers']:
            return False
        # bait is already bought
        if bait in self.modifiers:
            return False

        baitObj = gamedef.GAME['modifiers'][bait]
        # not enough money
        if not self.hasEnoughFor(baitObj['price']):
            return False

        self.money -= baitObj['price']
        self.modifiers[bait] = False # not selected by default
        self.savePlayer()
        return True

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

