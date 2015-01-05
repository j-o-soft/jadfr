from .categories import urls as categories_urls
from .feeds import urls as feeds_urls
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'feed/', include(feeds_urls)),
    url(r'^category/', include(categories_urls))
)
