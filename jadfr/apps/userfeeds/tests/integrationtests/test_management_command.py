from django.contrib.auth.models import User
from django.test import TestCase
from django.core import management
from djangofeeds.models import Category as BaseFeedCategory
from mock import patch

from apps.userfeeds.services import FeedWriteService, CategoryInfo, FeedInfo
from apps.userfeeds.models import UserFeed, UserCategory


class ImportFeedBase(TestCase):

    fixtures = ['apps/userfeeds/tests/integrationtests/fixtures/importfeeds.json']


class TestManagementCommand(ImportFeedBase):

    @patch('apps.userfeeds.management.commands.import_feeds.Worker._parse_file')
    # we don't give a valid file so we have to mock the parse method to make it pass
    def test_command_calls_service_class(self, parse_mock):
        """
                tests that the save method in the feedwriter is called
                """
        command = 'import_feeds'
        with patch('apps.userfeeds.management.commands.import_feeds.FeedWriteService.rsave') as service_mock:
            management.call_command(command, file='somefile', user=User.objects.get().username)
        service_mock.assertCalledOnce()


class TestFeedWriteService(ImportFeedBase):

    def setUp(self):
        BaseFeedCategory.objects.create(name=UserFeed.default_base_feed_category_name)

    def test_category_gets_created(self):

        user = User.objects.get()
        service = FeedWriteService(user)

        assert UserCategory.objects.count() == 0

        category_result = CategoryInfo(name='foo')
        service.rsave([category_result])

        category = UserCategory.objects.all().get()
        assert category.name == category_result.name

    def test_feed_gets_created(self):

        user = User.objects.get()
        service = FeedWriteService(user)

        assert UserFeed.objects.all().count() == 0
        category_result = CategoryInfo(name='cat_foo')
        feed_result = FeedInfo(
            feed_type='type',
            feed_url='xmlUrl',
            html_url='htmlUrl',
            title='title',
            category=category_result
        )

        service.rsave([category_result])
        service.rsave([feed_result])
        users_feed = UserFeed.objects.all().get()
        assert users_feed.user == user
        base_feed = users_feed.feed
        assert base_feed.name == feed_result.title
        assert base_feed.feed_url == feed_result.feed_url
