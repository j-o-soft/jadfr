from .feeds import urls as feeds_urls
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'feed/', include(feeds_urls)),
)
