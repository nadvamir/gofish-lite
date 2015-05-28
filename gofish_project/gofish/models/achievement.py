from django.db import models

class Achievement(models.Model):
    player = models.ForeignKey('gofish.Player')
    # name of an achievement
    name   = models.TextField()
    # value of an achievement
    value  = models.FloatField()
    # stars rating when relevant
    rating = models.IntegerField()

    #############################################################
    # Achievement API
    #############################################################
    # insert or update achievement, if better
    @staticmethod
    def upsert(player, name, value=0.0, rating=0):
        ach = None
        # update if exists
        try:
            ach = Achievement.objects\
                    .get(player=player, name=name)
            if ach.value < value:
                ach.value  = value
                ach.rating = rating
                ach.save()
        # insert if doesn't
        except Achievement.DoesNotExist:
            Achievement(
                    player = player,
                    name   = name,
                    value  = value,
                    rating = rating).save()

    # return top score for some achievement
    @staticmethod
    def getTop(name, N=1):
        return Achievement.objects\
                .filter(name=name)\
                .order_by('-value')[:N]

    # serialisation
    def toDict(self):
        return {
            'name'   : self.name,
            'value'  : self.value,
            'rating' : self.rating,
        }

    #############################################################
    # Django boilerplate
    #############################################################
    # this has to be included to make Django realise
    # that this model belongs to the app
    class Meta:
        app_label = 'gofish'

