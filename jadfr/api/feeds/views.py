from api.feeds.serializers import UserFeedSerializer
from apps.userfeeds.models import UserFeed
from rest_framework.generics import ListAPIView


class FeedList(ListAPIView):
    queryset = UserFeed.objects.all()
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class FeedEntries(ListAPIView):
    pass