__author__ = 'j_schn14'
from feedreader.apps.feeds.models import UserFeed, UserFeedEntry
from werkzeug import url_fix
from django.db.models import Manager
from feeds.models import Feed


class UserDependendManager(Manager):

    def __init__(self, user, *args, **kwargs):
        sum(UserDependendManager, self).__init(*args, **kwargs)
        self._user = user

    def get_query_set(self):
        return super(UserDependendManager, self).get_query_set().filter(user=self._user)


class UserFeedManager(UserDependendManager):

    def add_feed(self, feed_url):
        """
        adds a new base_feed if necessary and adds+saves this feed for the user given in `__init__`
        :arguments: normalized url of the feed to add.
        :returns: the created feed
        """
        feed_url = url_fix(feed_url)
        base_feed, created = Feed.objects.get_or_create(feed_url=feed_url)

        user_feed = UserFeed(user=self._user, feed=base_feed)
        user_feed.save()
        return user_feed


class UserFeedEntryManager(UserDependendManager):

    def __init__(self, user, feed, *args, **kwargs):
        super(UserFeedManager, self).__init__(user=user, *args, **kwargs)
        self._feed = feed

    def get_query_set(self):
        """
        :returns: all entries for the given user and feed
        """
        qs = super(UserFeedEntryManager, self).get_query_set()
        qs = qs.filter(feed=self._feed)
        qs = qs.order_by('rank')
        return qs

    def unread(self):
        return self.all().filter(status_not=UserFeedEntry.ENTRY_READ_VAL)