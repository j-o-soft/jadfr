from django.contrib.auth.models import User
from django.test import TestCase
from mock import  patch
from django.core import management

from apps.userfeeds.management.commands.import_feeds import Worker


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
            management.call_command(command, file='somefile')
        service_mock.assertCalledOnce()


class TestFeedWriteService(ImportFeedBase):

    class OpmlHelperObject(object):

        def __init__(self, **kwargs):
            self.nodes = kwargs.pop('nodes', [])
            self.kwargs = kwargs

        def __getattr__(self, item):
            return self.kwargs[item]

        def __iter__(self):
            for node in self.nodes:
                yield node



    file_name = 'foobar'

    def setUp(self):
        user_name = User.objects.all().get()
        self.worker = Worker(user_name=user_name.username,
                             file_name=self.file_name)

    def test_category_gets_created(self):

        category_result = TestFeedWriteService.OpmlHelperObject(title='foo')

        with patch('apps.userfeeds.management.commands.import_feeds.opml.parse',
                   return_value=category_result):
            self.worker.execute()

    def test_feed_gets_created(self):
        feed_result = TestFeedWriteService.OpmlHelperObject(title='foo')

        with patch('apps.userfeeds.management.commands.import_feeds.opml.parse',
                   return_value=feed_result):
            self.worker.execute()