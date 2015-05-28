from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gofish/', include('gofish.urls')),
    url(r'^charts/', include('charts.urls')),
    url(r'^convert/', include('lazysignup.urls')),
    url(r'^$', lambda r: HttpResponseRedirect('gofish/')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
