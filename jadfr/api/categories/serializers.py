__author__ = 'j_schn14'
from apps.usercategories.models import Category
from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')
