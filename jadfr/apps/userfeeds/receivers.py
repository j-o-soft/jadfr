from django.db.models.signals import pre_save, post_save
from .models import UserFeedEntry, UserFeed
from feeds.models import Entry


def update_rank(sender, *args, **kwargs):
    instance = kwargs['instance']
    instance.update_rank()

pre_save.connect(update_rank, UserFeedEntry)


#maybe this code should be moved, because it's not a signal handler for a jadfr model.
def base_feed_post_save_hadler(sender, *args, **kwargs):
    """
    Takes all active user_feeds to which this entry belongs and creates the corresponding
    user_feed_entry.
    """
    base_feed_instance = kwargs['instance']
    user_feeds = UserFeed.objects.filter(feed=base_feed_instance.feed, activce=True)
    for user_feed in user_feeds:
        user_feed_entry, created = UserFeedEntry.objects.get_or_create(feed=user_feed, entry=base_feed_instance)
        if not created:
            user_feed_entry.save()

post_save.connect(base_feed_post_save_hadler, Entry)