from django.dispatch import receiver
from djangofeeds.models import Post as FeedEntry
from django.db.models.signals import post_save

from apps.userfeeds import  tasks


@receiver(post_save, sender=FeedEntry)
def feedentry_post_saved(instance, **kwargs):
    """
    Saves the feed entry for every user feed.
    :param instance:
    :param kwargs:
    :return:
    """
    tasks.save_user_feed_entries(instance)