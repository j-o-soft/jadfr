from apps.userfeeds.services import CategoryInfo, FeedInfo, FeedWriteService
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from optparse import make_option

import logging
import opml

__author__ = 'j_schn14'
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--user', '-u', action="store", type="string", dest="user"),
        make_option('--file', '-f', action="store", type="string", dest="filename"),
        make_option('--quiet', '-q', action="store_false", dest="verbose"),
        make_option('--dry-run', '-d', action="store_true", dest="dry_run"),
    )

    def __int__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.user = None

    def handle(self, *args, **options):
        """
        reads feed information from opml file and stores them in the database
        """
        verbose = options.get('verbose')
        user = options.get('user')
        if not user:
            self.parser.error("username is required")
        file_name = options.get('filename')
        if not file_name:
            self.parser.error("filename is required")
        dry_run = options.get('dry_run')

        # if a user is give, select it from the db
        worker = Worker(user_name=user,
                        file_name=file_name,
                        verbose=verbose,
                        dry_run=dry_run)
        worker.execute()


class Worker(object):

    def __init__(self, user_name, file_name, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.file_name = file_name
        self.verbose = verbose
        if user_name:
            self.user = User.objects.get(username=user_name)
        self.service_class = FeedWriteService(user=self.user, dry_run=self.dry_run, logger=logger,)

    def execute(self):
        # read the data from file
        data = self._parse_file(self.file_name)
        # store it to the databaase
        self.service_class.rsave(data=data)

    def _parse_file(self, file_name):
        """
        creates nested structure of feedInfos and feedcategories from the ompl file
        :param file_name: the file to pare
        :return: a FeedInfo Object containing all Information from the file
        """
        outline = opml.parse(file_name)
        return self.get_feeds_from_outline(outline)

    def get_feeds_from_outline(self, outline):
        """
        helper function to create the nested feedInfo Object(s)
        :param outline: parsed opml file (or node inside it)
        :return: a FeedInfo object for the data below the node
        """
        result = CategoryInfo(outline.title)
        for o in outline:
            values = o._root.find('[@xmlUrl]')
            if values is not None:
                result.add(FeedInfo(
                    feed_type=values.get('type'),
                    feed_url=values.get('xmlUrl'),
                    html_url=values.get('htmlUrl'),
                    title=values.get('title'),
                    category=result
                ))
            else:
                result.add(self.get_feeds_from_outline(o))
        return result
