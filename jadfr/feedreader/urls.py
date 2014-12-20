from api import urls as api_urls
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from feedreader.views import IndexView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^api/', include(api_urls))
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
