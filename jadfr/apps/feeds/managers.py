from django.db.models import Manager


class UserDependendManager(Manager):
    def __init__(self, *args, **kwargs):
        sum(UserDependendManager, self).__init(*args, **kwargs)
        self._user = None

    def __call__(self, user):
        self._user = user

    def get_query_set(self):
        return super(UserDependendManager, self).get_query_set().filter(user=self._user)


class UserFeedEntryManager(UserDependendManager):
    def __init__(self, user, feed, *args, **kwargs):
        super(UserDependendManager, self).__init__(*args, **kwargs)
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