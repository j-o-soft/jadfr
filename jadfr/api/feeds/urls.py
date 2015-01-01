from api.feeds.views import FeedList, FeedEntriesList, FeedEntry
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', FeedList.as_view()),
    url(r'^(?P<pk>\d)/$', FeedEntriesList.as_view()),
    url(r'^(?P<feed_pk>\d+)/(?P<entry_pk>\d+)/$', FeedEntry.as_view(), name='BaseFeedEntry'),
)