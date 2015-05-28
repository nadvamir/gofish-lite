from django.conf.urls import patterns, url
from gofish import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),

        # old api
        # start a new game round
        url(r'^api/start/(?P<level>\w+)/$', views.start, name='start'),
        # end the current game round preemptively
        url(r'^api/end/$', views.end, name='end'),
        # execute action
        url(r'^api/action/(?P<action>\w+)/(?P<par>[\w,]+)/$', views.action, name='action'),

        # next gen api
        # get game info for a home screen
        url(r'^api/v2/home/$', views.v2home, name='v2home'),
        # get player information
        url(r'^api/v2/player/$', views.v2player, name='v2player'),
        # get game instance if it already exists
        url(r'^api/v2/game/$', views.v2game, name='v2game'),
        # return trophies
        url(r'^api/v2/trophies/$', views.v2trophies, name='v2trophies'),
        )
