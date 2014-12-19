from apps.userfeeds.models import UserFeed
from celery.canvas import group
from djangofeeds.tasks import refresh_feed
from logging import getLogger
from feedreader.celery import app

logger = getLogger(__name__)


def load_feeds(user=None):
    user_feeds = UserFeed.objects.all()
    if user:
        user_feeds = user_feeds.filter(user=user)
    feeds = set(user_feed.feed for user_feed in user_feeds)
    logger.debug('found %s feeds to update for user %s.', len(feeds), user)
    group(load_feed.s(feed) for feed in feeds).delay()


@app.task
def load_feed(feed):
    # small hacke needet to get djangofees task working without the
    # task decorator
    refresh_feed.get_logger = lambda **kwargs: logger
    refresh_feed(feed_url=feed.feed_url)




