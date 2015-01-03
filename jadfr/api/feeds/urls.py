from api.feeds.views import FeedList, FeedEntriesList, FeedEntry, AddFeed
from apps.userfeeds.models import UserFeedEntry
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', FeedList.as_view(), name='FeedList'),
    url(r'^new/$', FeedEntriesList.as_view(),
        {'filters': {
            'status__lte': UserFeedEntry.ENTRY_UNREAD_VAL}
         },
        name='FeedList'),
    url(r'^(?P<pk>\d)/$', FeedEntriesList.as_view(), name='BaseFeed'),
    url(r'^(?P<feed_pk>\d+)/(?P<entry_pk>\d+)/$', FeedEntry.as_view(), name='BaseFeedEntry'),
    url(r'^add/', AddFeed.as_view()),
)