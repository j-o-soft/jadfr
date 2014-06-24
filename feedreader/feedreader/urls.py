from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^login/$', login, {'template_name': 'account/login.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
