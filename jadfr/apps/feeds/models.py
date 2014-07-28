__author__ = 'j_schn14'
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, ForeignKey, IntegerField, ManyToManyField
from feeds.models import Entry, Feed, Category


class UserFeed(Model):


    feed = ForeignKey(Feed)
    user = ForeignKey(User)
    categories = ManyToManyField(Category)


class UserFeedEntry(Model):
    ENTRY_NEW_VAL = 0
    ENTRY_UNREAD_VAL = 1
    ENTRY_READ_VAL = 2

    Feed_Entry_Choices = (
        (ENTRY_NEW_VAL, _('new')),
        (ENTRY_UNREAD_VAL, _('unread')),
        (ENTRY_READ_VAL, _('read'))
    )

    feed = ForeignKey(UserFeed)
    entry = ForeignKey(Entry)
    status = IntegerField(choices=Feed_Entry_Choices)
    rank = IntegerField(null=False, blank=False, default=0)

    def update_rank(self):
        """
        TODO: implement an rank function to order entries
        the rank function should depend on the date, number of time other users read this entry
        and the number of times the user read entries in the same category the feed belongs to.
        """
        pass