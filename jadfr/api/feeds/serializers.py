from apps.feeds.models import UserFeed
from feeds.models import Feed

__author__ = 'j_schn14'
from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'name', 'url', 'feed_url', 'category')


class UserFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeed
        fields = ('id', 'feed', 'category')