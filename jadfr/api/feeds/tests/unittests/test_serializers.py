from api.feeds.serializers import RecursiveField, ProxyModelSerializer
from django.db.models import Model, ForeignKey, CharField
from django.test import TestCase
from rest_framework.serializers import Serializer, ModelSerializer
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
__author__ = 'j_schn14'


class TestProxyModelSerializer(TestCase):

    def setUp(self):
        class M1(Model):
            field = CharField()

        class M2(Model):
            field = CharField()
            proxy = ForeignKey(M1)

        class CSerializerM1(ModelSerializer):
            class Meta:
                model = M1
                fields = 'field',

        class CSerializerM2(ProxyModelSerializer):
            class Meta:
                model = M2
                fields = tuple()
                proxy_fields = 'field',
                proxy = 'proxy'

        self.M1 = M1
        self.M2 = M2

        self.SerializerM1 = CSerializerM1
        self.SerializerM2 = CSerializerM2

    def test_proxyed_val(self):
        # do some setup stuff.
        fld1 = 'field1'
        fld2 = 'field2'
        m1 = self.M1(field=fld1)
        m2 = self.M2(field=fld2, proxy=m1)
        # first try: serialize m2 which has to have field2 as value of field2 after serialisation
        data_serializer = self.SerializerM2(m2)
        json = JSONRenderer().render(data_serializer.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)
        for field_name, value in data.iteritems():
            assert getattr(m2, field_name) == value
        # second try: serialize m2prime which has the proxyed value field1.
        m2prime = self.M2(field='', proxy=m1)
        data_serializer = self.SerializerM2(m2prime)
        json = JSONRenderer().render(data_serializer.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)
        for field_name, value in data.iteritems():
            assert getattr(m1, field_name) == value