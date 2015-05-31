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
            'numGames'  : self.numGames
        }

    def __unicode__(self):
        return ','.join(map(str, [
            self.user.id, self.numGames, self.level
        ]))

    #############################################################
    # helpers
    #############################################################
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
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

