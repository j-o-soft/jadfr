from apps.usercategories.models import Category
from apps.userfeeds.models import UserFeed

import logging
from djangofeeds.models import Feed
from djangofeeds.models import Category as BaseFeedCategory


class FeedWriteService(object):

    def __init__(self, logger=None, dry_run=False):
        self.logger = logger or logging.getLogger(__name__)
        self.dry_run = dry_run

    def rsave(self, data):
        """
        saves the Information of a FeedInfo object recursively  to the database
        :param data: Items to save FeedInfoObject
        :param dry_run: if false, no db operations is performed
        """
        for item in data:
            if isinstance(item, FeedInfo):
                save_func = self.save_feed
            else:
                save_func = self.save_category
            if self.verbose:
                self.logger.info("Saving %s", item)
            save_func(item, dry_run=self.dry_run)

    def save_feed(self, feed_item):
        try:
            feed = Feed.objects.get(feed_url=feed_item.feed_url)
        except Feed.DoesNotExist:
            feed = Feed(
                feed_url=feed_item.feed_url,
                name=feed_item.title
            )
            if not self.dry_run:
                feed.save()
                feed.categories.add(BaseFeedCategory.objects.get(name=UserFeed.default_base_feed_category_name))
        try:
            user_feed = UserFeed.objects.get(feed=feed, user=self.user)
        except UserFeed.DoesNotExist:
            user_feed = UserFeed.objects.create(
                feed=feed,
                user=self.user
            )
        feed_category = Category.objects.get(name=feed_item.category.name)
        user_feed.categories.add(feed_category)
        if not self.dry_run:
            user_feed.save()

    def save_category(self, category_item):
        if not Category.objects.filter(name=category_item.name).exists():
            category = Category(name=category_item.name)
            if not self.dry_run:
                category.save()
        self.save(category_item)


class FeedInfo(object):
    def __init__(self,
                 feed_type,
                feed_url,
                html_url,
                title,
                category
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
