from apps.userfeeds.models import UserFeed
from celery.canvas import group
from feedreader.celery import app


def load_feeds(user=None):
    user_feeds = UserFeed.objects.all()
    if user:
        user_feeds = user_feeds.filter(user=user)
    feeds = set(user_feed.feed for user_feed in user_feeds)
    group(load_feed_task.s(feed) for feed in feeds)


@app.task
def load_feed_task(feed):
    feed.update()

