from unittest import TestCase
from printen.mixins import ElasticsearchIndexMixin
import printen.config


class ConfigTests(TestCase):
    def tearDown(self):
        # Ensure we have a clean settings object
        # between runs
        printen.config.settings = printen.config.SettingsObject()

    def test_settings_setup(self):
        self.assertTrue(
            isinstance(printen.config.settings, printen.config.SettingsObject)
        )

    def test_configure_settings(self):
        with self.assertRaises(AttributeError):
            printen.config.settings.foo
        printen.config.configure({'foo': 'bar'})
        self.assertEqual(printen.config.settings.foo, 'bar')

    def test_get_search_types(self):
        class SearchTypeClass(ElasticsearchIndexMixin):
            pass

        printen.config.configure({
            'ELASTICSEARCH_TYPE_CLASSES': [
                SearchTypeClass,
            ]
        })

        self.assertIs(
            printen.config._search_types,
            None
        )

        search_types = printen.config.get_search_types()

        self.assertEqual(
            search_types,
            {
                'SearchTypeClass': SearchTypeClass
            }
        )

        self.assertEqual(
            printen.config._search_types,
            search_types
        )
