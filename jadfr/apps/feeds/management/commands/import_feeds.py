import opml

__author__ = 'j_schn14'

from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--user', '-u', action="store", type="string", dest="user"),
        make_option('--file', '-f', action="store", type="string", dest="filename"),
        make_option('--quiet', '-q', action="store_false", dest="verbose"),
        make_option('--dry-run', '-d', action="store_true", dest="dry_run"),
    )

    def handle(self, *args, **options):

        user = options.get('user')
        file_name = options.get('filename')
        verbose = options.get('verbose')
        dry_run = options.get('dry_run')

        self.parse_file(file_name)

    def parse_file(self, file_name):
        outline = opml.parse(file_name)
        return self.get_feeds_from_outline(outline)

    def get_feeds_from_outline(self, outline):
        result = CategoryInfo(name=outline.title)
        for o in outline:
            values = o._root.find('[@xmlUrl]')
            if values is not None:
                result.add(FeedInfo(
                    feed_type=values.get('type'),
                    feed_url=values.get('xmlUrl'),
                    html_url=values.get('htmlUrl'),
                    title=values.get('title')
                ))
            else:
                result.add(self.get_feeds_from_outline(o))
        return result


class FeedInfo(object):
    def __int__(self,
                feed_type,
                feed_url,
                html_url,
                title
    ):
        self.feed_type = feed_type
        self.feed_url = feed_url
        self.html_url = html_url
        self.title = title


class CategoryInfo(set):
    name = ''

    def __int__(self, name, **kwargs):
        super(CategoryInfo, self).__init__()
        self.name = name
        if 'items' in kwargs:
            self.add(item for item in kwargs['items'])