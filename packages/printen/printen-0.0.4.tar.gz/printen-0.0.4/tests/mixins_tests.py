from unittest import TestCase
from elasticsearch import Elasticsearch
from printen.exceptions import MissingObjectError
from printen.mixins import (
    ElasticsearchIndexMixin,
    DjangoElasticsearchIndexMixin,
    PeeweeElasticsearchIndexMixin
)
import printen.config


ELASTICSEARCH_SETTINGS = {
    'ELASTICSEARCH_DELETE_OLD_INDICES': True,
    'ELASTICSEARCH_INDEX_NAME': 'test',
    'ELASTICSEARCH_TYPE_CLASSES': [],
    'ELASTICSEARCH_CONNECTION_PARAMS': {
        'hosts': 'http://127.0.0.1:9200',
    },
}


class MixinTests(TestCase):
    def tearDown(self):
        # Ensure we have a clean settings object
        # between runs
        printen.config.settings = printen.config.SettingsObject()

    def test_get_es(self):
        # An unconfigured model should not have
        # an es object.
        with self.assertRaises(AttributeError):
            ElasticsearchIndexMixin.get_es()

        printen.config.configure(ELASTICSEARCH_SETTINGS)

        self.assertTrue(isinstance(
            ElasticsearchIndexMixin.get_es(),
            Elasticsearch
        ))

    def test_get_es_connection_settings(self):
        with self.assertRaises(AttributeError):
            ElasticsearchIndexMixin.get_es_connection_settings()

        printen.config.configure(ELASTICSEARCH_SETTINGS)

        self.assertEqual(
            ElasticsearchIndexMixin.get_es_connection_settings(),
            ELASTICSEARCH_SETTINGS['ELASTICSEARCH_CONNECTION_PARAMS']
        )

    def test_get_index_name(self):
        self.assertEqual(
            ElasticsearchIndexMixin.get_index_name(),
            'index'
        )

        printen.config.configure(ELASTICSEARCH_SETTINGS)

        self.assertEqual(
            ElasticsearchIndexMixin.get_index_name(),
            ELASTICSEARCH_SETTINGS['ELASTICSEARCH_INDEX_NAME']
        )

    def test_get_document_id(self):
        # The base class doesn't implement this at all
        with self.assertRaises(NotImplementedError):
            ElasticsearchIndexMixin.get_document_id(object())

        # The Django (and Peewee) versions do - but of course
        # an object without the right attribute will fail.
        with self.assertRaises(MissingObjectError):
            DjangoElasticsearchIndexMixin.get_document_id(object())

        with self.assertRaises(MissingObjectError):
            PeeweeElasticsearchIndexMixin.get_document_id(object())

        # Now we create objects we expect to succeed:
        class Foo(object):
            pass
        foo = Foo()
        foo.pk = 1
        self.assertEqual(
            DjangoElasticsearchIndexMixin.get_document_id(foo),
            1
        )

        class Bar(object):
            pass
        bar = Bar()
        bar._meta = Bar()
        bar._meta.primary_key = Bar()
        bar._meta.primary_key.name = 'baz'
        bar.baz = 1
        self.assertEqual(
            PeeweeElasticsearchIndexMixin.get_document_id(bar),
            1
        )

    def test_get_type_name(self):
        self.assertEqual(
            ElasticsearchIndexMixin.get_type_name(),
            'ElasticsearchIndexMixin'
        )

        class Object(object):
            pass
        DjangoElasticsearchIndexMixin._meta = Object()
        DjangoElasticsearchIndexMixin._meta.app_label = 'foo'
        DjangoElasticsearchIndexMixin._meta.model_name = 'bar'
        self.assertEqual(
            DjangoElasticsearchIndexMixin.get_type_name(),
            'foo.bar'
        )

        PeeweeElasticsearchIndexMixin.model = Object()
        PeeweeElasticsearchIndexMixin.model._meta = Object()
        PeeweeElasticsearchIndexMixin.model._meta.name = 'foo'
        self.assertEqual(
            PeeweeElasticsearchIndexMixin.get_type_name(),
            'foo'
        )
