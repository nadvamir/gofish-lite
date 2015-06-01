from django.conf.urls import patterns, url
from charts import views

urlpatterns = patterns('',
        # index page, to show the options
        url(r'^$', views.index, name='index'),

        # consumes log and creates database entries from it
        url(r'^parse_log/$', views.parseLog),
        # consumes end log and creates database entries from it
        url(r'^parse_end_log/$', views.parseEndLog),
        # visualiser of individual user data
        url(r'^data_by_user/$', views.dataByUser),
        # visualiser of aggregated data
        url(r'^data_aggregated/$', views.dataAggregated),
        # visualiser of endgame data
        url(r'^data_endgame/$', views.dataEndgame),

        # api call to get specific data
        url(r'^api/get_data/$', views.getData),
        # api call for bar chart data
        url(r'^api/get_bar_data/$', views.getBarData),
        # api call for box plot data
        url(r'^api/get_box_data/$', views.getBoxData),
        # api call for endgame bar chart data
        url(r'^api/get_end_data/$', views.getEndData),
        # api call for endgame box chart data
        url(r'^api/get_end_box_data/$', views.getEndBoxData),
)
