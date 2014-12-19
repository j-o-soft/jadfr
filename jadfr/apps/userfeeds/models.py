__author__ = 'j_schn14'
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, ForeignKey, IntegerField, ManyToManyField, CharField, BooleanField
from djangofeeds.models import Post, Feed

from apps.usercategories.models import Category


class UserFeed(Model):
    default_base_feed_category_name = 'default'

    feed = ForeignKey(Feed)
    user = ForeignKey(User)
    categories = ManyToManyField(Category, null=True)
    # the user given name can differ from the original name
    name = CharField(max_length=255, null=True)
    active = BooleanField(default=True)

    @property
    def display_name(self):
        # because or returns the first not None value the following works
        return self.name or self.feed.name


class UserFeedEntry(Model):
    ENTRY_NEW_VAL = 0
    ENTRY_MARKED_VAL = 1
    ENTRY_UNREAD_VAL = 2
    ENTRY_SEEN_VAL = 3
    ENTRY_READ_VAL = 4

    Feed_Entry_Choices = (
        (ENTRY_NEW_VAL, _('new')),
        (ENTRY_UNREAD_VAL, _('unread')),
        (ENTRY_READ_VAL, _('read')),
        (ENTRY_SEEN_VAL, _('seen')),
        (ENTRY_MARKED_VAL, _('remember'))
    )

    feed = ForeignKey(UserFeed)
    entry = ForeignKey(Post)
    status = IntegerField(choices=Feed_Entry_Choices, default=ENTRY_NEW_VAL)
    rank = IntegerField(null=False, blank=False, default=0)

    def update_rank(self):
        """
        TODO: implement an rank function to order entries
        the rank function should depend on the date, number of time other users read this entry
        and the number of times the user read entries in the same category the feed belongs to.
        """
        pass