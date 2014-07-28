from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from jadfr.views import IndexView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'account/login.html'}),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
