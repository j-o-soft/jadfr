from api.feeds.serializers import UserFeedSerializer, UserFeedEntrySerializer
from apps.userfeeds.models import UserFeed, UserFeedEntry, UserCategory
from apps.userfeeds import tasks

from django.core.urlresolvers import reverse
from logging import getLogger
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView


logger = getLogger(__name__)


class FeedList(ListAPIView):

    queryset = UserFeed.objects.all()
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class FeedEntriesList(ListAPIView):
    queryset = UserFeedEntry.objects.all()(tasks.inc_entry_status)
    serializer_class = UserFeedEntrySerializer
    pagination_class = PageNumberPagination

    def __init__(self):
        self.pagination_class.page_size = 10

    def get_queryset(self):
        filters = self.kwargs.get('filters', {})
        feed_pk = self.kwargs.get('pk', None)
        if feed_pk:
            filters['feed_id'] = feed_pk
        filters['feed__user'] = self.request.user
        res = self.queryset.filter(**filters)
        return res


class FeedEntry(RetrieveAPIView):

    queryset = UserFeedEntry.objects.all()(tasks.inc_entry_status)
    serializer_class = UserFeedEntrySerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(feed__user=user)

    def get_object(self):
        feed_pk = self.kwargs['feed_pk']
        entry_pk = self.kwargs['entry_pk']
        obj = self.get_queryset().get(pk=entry_pk, feed_id=feed_pk)
        return obj


class AddFeed(APIView):

    def post(self, request, *args, **kwargs):
        feed_urls = [self.request.DATA.get('url', None)]
        if not feed_urls:
            feed_urls = self.request.DATA['urls']
        user = self.request.user
        tasks.add_feeds(user, feed_urls)
        headers = self.get_success_headers(feed_urls)
        return Response(feed_urls, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        # I don't like this, because it's not RESTFull, but I don't know how to
        # to manage it, because ot cam add more than one feed and it is a celery task in
        try:
            base_url = reverse('FeedList')
            return {'Location': base_url}
        except (TypeError, KeyError):
            return {}


class CategoryView(FeedEntriesList):

    category_ids = []

    def filter_queryset(self, qs):
        return qs

    def get(self, request, category_ids):
        self.category_ids = filter(lambda s: s, category_ids.split('/'))
        return super(CategoryView, self).get(request)