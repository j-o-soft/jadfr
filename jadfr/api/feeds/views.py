from api.feeds.serializers import UserFeedSerializer, UserFeedEntrySerializer
from apps.userfeeds.models import UserFeed, UserFeedEntry
from rest_framework.generics import ListAPIView, RetrieveAPIView


class FeedList(ListAPIView):
    queryset = UserFeed.objects.all()
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class FeedEntriesList(ListAPIView):
    queryset = UserFeedEntry.objects.all()
    serializer_class = UserFeedEntrySerializer

    def get_queryset(self):
        feed_pk = self.kwargs['pk']
        user = self.request.user
        return self.queryset.filter(feed_id=feed_pk, feed__user=user)


class FeedEntry(RetrieveAPIView):

    queryset = UserFeedEntry.objects.all()
    serializer_class = UserFeedEntrySerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(feed__user=user)

    def get_object(self):
        feed_pk  = self.kwargs['feed_pk']
        entry_pk = self.kwargs['entry_pk']
        obj = self.get_queryset().get(pk=entry_pk, feed_id=feed_pk)
        return obj