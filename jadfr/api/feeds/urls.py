from api.feeds.views import FeedList, FeedEntries
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', FeedList.as_view()),
    url(r'^/(?P<pk>\d)$', FeedEntries.as_view()),
)

