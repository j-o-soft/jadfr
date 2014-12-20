from apps.userfeeds.models import UserFeed
from djangofeeds.models import Feed

from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'name', 'url', 'feed_url', 'category')


class UserFeedSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserFeed
        fields = ('id', 'feed', 'name', 'categories')

    def get_name(self, obj):
        """
        returns a feeds name if present otherwise the name of the base feed.
        :param obj: a Userfeedobject.
        :return: a feeds name
        """
        return obj.name or obj.feed.name