from apps.userfeeds.models import UserFeed, UserFeedEntry
from apps.userfeeds.services import FeedWriteService, FeedInformationService
from celery.canvas import group
from djangofeeds.tasks import refresh_feed
from logging import getLogger
from feedreader.celery import app

logger = getLogger(__name__)


def update_feed_status(item, status):
    update_feed_status_task.delay(item, status)


def inc_entry_status(item):
    """
    sets the status to seen for new or unread items
    """
    logger.info('Status of %s == %s', item.pk, item.status)
    if item.status in (UserFeedEntry.ENTRY_NEW_VAL, UserFeedEntry.ENTRY_UNREAD_VAL):
        status = UserFeedEntry.ENTRY_SEEN_VAL
        update_feed_status_task.delay(item, status)

@app.task
def update_feed_status_task(item, status):
    item.status = status
    item.save()
    logger.info('Status of %s set to %s', item, status)


def add_feeds(user, feedurls, fuzzy=True, dry_run=False):
    write_task = write_feed_task.s(user=user,  dry_run=dry_run)
    info_task = get_feed_info_from_url_task.s(fuzzy=fuzzy)

    group((info_task | write_task)(feedurl) for feedurl in feedurls).delay()


def add_feed(user, feedurl, fuzzy=True, logger=logger, dry_run=False):
    write_task = write_feed_task.s(user=user,  dry_run=dry_run)
    info_task = get_feed_info_from_url_task.s(fuzzy=fuzzy)

    (info_task | write_task).delay(feedurl)

@app.task
def write_feed_task(feed_info, user, dry_run, logger=logger):
    feed_wrtier_serice = FeedWriteService(user, logger, dry_run)
    return feed_wrtier_serice.rsave(feed_info)

@app.task
def get_feed_info_from_url_task(feed_url, fuzzy=False):
    info_service = FeedInformationService(feed_url, accept_fuzzy=fuzzy)
    return info_service.parse()


def load_feeds(user=None):
    """
    updates all feeds (if a user is given, only the feeds of this user are updatet
    :param user:  user which feeds should be updated, all user if not set
    """
    user_feeds = UserFeed.objects.all()
    if user:
        user_feeds = user_feeds.filter(user=user)
    feeds = set(user_feed.feed for user_feed in user_feeds)
    logger.debug('found %s feeds to update for user %s.', len(feeds), user)
    group(load_feed_task.s(feed) for feed in feeds).delay()


@app.task
def load_feed_task(feed):
    """
    Wrapper to update a feed.
    Wrapps the ``refresh_feed`` task from djangofeeds.
    :param feed: feed to update
    """
    # small hacke needet to get djangofees task working without the
    # task decorator
    refresh_feed.get_logger = lambda **kwargs: logger
    refresh_feed(feed_url=feed.feed_url)


def save_user_feed_entries(feed_entry):
    """
    delegates the new feeds to all users which have this as userfeed
    :param feed_entry: wich was updated
    """
    save_user_feed_entries_task.delay(feed_entry)


@app.task
def save_user_feed_entries_task(feed_entry):
    """
    stores the given feed entry for all users which have this feed as userfeed
    """
    base_feed = feed_entry.feed
    user_feeds = UserFeed.objects.filter(feed=base_feed)
    for item in user_feeds:
        save_user_feed_item_task.delay(user_feed=item, base_feed_entry=feed_entry)

@app.task
def save_user_feed_item_task(user_feed, base_feed_entry):
    user_feed_entry, created = UserFeedEntry.objects.get_or_create(feed=user_feed, entry=base_feed_entry)
    if created:
        logger.debug('created new FeedEntry of "%s" for user "%s"', base_feed_entry, user_feed.user)