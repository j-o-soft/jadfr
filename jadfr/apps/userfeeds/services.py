from apps.userfeeds.models import UserFeed, UserCategory

import feedfinder2
import feedparser
import logging
from djangofeeds.models import Feed
from djangofeeds.models import Category as BaseFeedCategory


class FeedWriteService(object):

    def __init__(self, user, logger=None, dry_run=False):
        self.logger = logger or logging.getLogger(__name__)
        self.dry_run = dry_run
        self.user = user

    def save(self, data):
        return self.rsave([data])

    def rsave(self, data):
        """
        saves the Information of a FeedInfo object recursively  to the database
        :param data: Items to save FeedInfoObject
        """
        for item in data:
            if isinstance(item, FeedInfo):
                save_func = self.save_feed
            else:
                save_func = self.save_category
                self.logger.info("Saving %s", item)
            save_func(item)

    def save_feed(self, feed_item):
        try:
            feed = Feed.objects.get(feed_url=feed_item.feed_url)
        except Feed.DoesNotExist:
            self.logger.info("Feed %s does not exist.", feed_item.feed_url)
            feed = Feed(
                feed_url=feed_item.feed_url,
                name=feed_item.title
            )
            if not self.dry_run:
                feed.save()
                self.logger.info('Feed saved')
                feed.categories.add(BaseFeedCategory.objects.get(name=UserFeed.default_base_feed_category_name))
        try:
            user_feed = UserFeed.objects.get(feed=feed, user=self.user)
        except UserFeed.DoesNotExist:
            user_feed = UserFeed.objects.create(
                feed=feed,
                user=self.user
            )
            self.logger.info('User feed %s created for %s', feed_item.feed_url, self.user)
        if feed_item.category:
            feed_category = UserCategory.objects.get(name=feed_item.category.name)
            user_feed.categories.add(feed_category)
            if not self.dry_run:
                user_feed.save()

    def save_category(self, category_item):
        if not UserCategory.objects.filter(name=category_item.name).exists():
            category = UserCategory(name=category_item.name)
            if not self.dry_run:
                category.save()
        self.rsave(category_item)


class FeedInfo(object):
    def __init__(self,
                 feed_type,
                 feed_url,
                 html_url,
                 title,
                 category=None
                 ):
        self.feed_type = feed_type
        self.feed_url = feed_url
        self.html_url = html_url
        self.title = title
        self.category = category

    def __str__(self):
        return self.title


class CategoryInfo(object):
    class CategoryInfoIter(object):

        def __init__(self, category_info):
            self._items = category_info._items

        def next(self):
            if not hasattr(self, '_iter'):
                self._iter = iter(self._items)
            return self._iter.next()

    def __init__(self, name, items=[]):
        super(CategoryInfo, self).__init__()
        self.name = name
        self._items = set()
        for item in items:
            self._items.add(item)

    def __iter__(self):
        return CategoryInfo.CategoryInfoIter(self)

    def add(self, item):
        self._items.add(item)

    def __str__(self):
        return self.name


class FeedInformationService(object):

    parse_exception_key = 'bozo_exception'

    def __init__(self, feed_url, accept_fuzzy=False):
        self.feed_url = feed_url
        self.accept_fuzzy = accept_fuzzy

    def parse(self):
        parse_result = feedparser.parse(self.feed_url)
        if self.accept_fuzzy and FeedInformationService.parse_exception_key in parse_result:
            feeds = feedfinder2.find_feeds(self.feed_url)
            parse_result = map(feedparser.parse, feeds)
        else:
            parse_result = [parse_result]

        result = [FeedInfo(
            feed_type=parsed_result['version'],
            feed_url=parsed_result['href'],
            html_url=parsed_result['feed']['link'],
            title=parsed_result['feed']['title']) for parsed_result in parse_result]
        return result
