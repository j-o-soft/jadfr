from collections import OrderedDict
from apps.userfeeds.models import UserFeed, UserFeedEntry, Category
from djangofeeds.models import Feed

from rest_framework import serializers


class ProxyModelSerializer(serializers.ModelSerializer):
    """
    This serializer acts like a model serializer but is extended for proxyied values:
    if a field definied in ``meta.proxyied_fields`` is not set in a model, the value
    of from the ``proxy_elemnt`` is used.

    ``meta.proxied_fields`` must be a dict or iterable. If its a dict, the key represents the name
    if the field, the value if a exception is raised if the field is not found in the base model.
    if it's a iterable the value of ``meta.raises`` is used. default of ``meta.raises``  is ``False``
    """

    @classmethod
    def _build_proxy_accessor(cls, field_name, proxy_item, raise_if_not_existent=False):
        """
        Build the getter methods for the proxied fields
        """

        def get_proxyied_value(obj):
            if raise_if_not_existent and not hasattr(obj, field_name):
                raise AttributeError()
            val = getattr(obj, field_name, None)
            if not val:
                proxy_element = getattr(obj, proxy_item)
                val = getattr(proxy_element, field_name)
            return val
        return get_proxyied_value

    def __new__(cls, *args, **kwargs):
        return_cls = super(ProxyModelSerializer, cls).__new__(cls, *args, **kwargs)
        if not hasattr(return_cls, '_declared_fields'):
            return_cls._declared_fields = OrderedDict()
        meta = getattr(cls, 'Meta', None)
        proxy_item = meta.proxy
        fields = meta.fields
        raises = getattr(meta, 'raises', False)
        if isinstance(fields, tuple):
            fields = [x for x in fields]
        if not hasattr(meta, 'fields'):
            meta.fields = []
        proxy_fields = meta.proxy_fields
        if not isinstance(proxy_fields, dict):
            proxy_fields = {field_name: raises for field_name in proxy_fields}
        for field_name, raise_ex in proxy_fields.iteritems():
            name = "get_%s" % field_name
            field = serializers.SerializerMethodField()
            func = ProxyModelSerializer._build_proxy_accessor(field_name, proxy_item, raise_if_not_existent=raise_ex)
            setattr(return_cls, field_name, field)
            setattr(return_cls, name, func)
            if field_name not in meta.fields:
                fields.append(field_name)
            return_cls._declared_fields[field_name] = field
        meta.fields = fields
        return return_cls


class RecursiveField(serializers.Serializer):
        def to_native(self, value):
            return self.parent.to_native(value)


class CategorySerializer(serializers.ModelSerializer):

    parent = RecursiveField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class UserFeedEntrySerializer(ProxyModelSerializer):

    class Meta:
        model = UserFeedEntry
        fields = ('status',)
        proxy_fields = ('title', 'link', 'content', 'author', 'date_published')
        proxy = 'entry'


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'name', 'url', 'feed_url', 'category')


class UserFeedSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    feed_entries = UserFeedEntrySerializer(source='userfeedentry_set', many=True)

    class Meta:
        model = UserFeed
        fields = ('id', 'feed_entries', 'name', 'categories')

    def get_name(self, obj):
        """
        returns a feeds name if present otherwise the name of the base feed.
        :param obj: a Userfeedobject.
        :return: a feeds name
        """
        return obj.name or obj.feed.name


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')
