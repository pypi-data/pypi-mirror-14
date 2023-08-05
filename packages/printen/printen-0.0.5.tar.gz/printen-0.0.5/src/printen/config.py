"""
An example configuration:

    ELASTICSEARCH_SETTINGS = {
        'ELASTICSEARCH_DELETE_OLD_INDICES': True,
        'ELASTICSEARCH_INDEX_NAME': env(
            'ELASTICSEARCH_INDEX_NAME',
            'example'
        ),
        'ELASTICSEARCH_TYPE_CLASSES': [
            'api.search.VideoSearch',
            'api.search.PlaylistSearch'
        ],
        'ELASTICSEARCH_CONNECTION_PARAMS': {
            'hosts': env(
                'ELASTICSEARCH_SERVER',
                'http://127.0.0.1:9200'
            ),
        },
    }
"""

import importlib
import inspect


class SettingsObject(object):
    def __init__(self, *args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


def configure(new_settings):
    global settings
    settings = SettingsObject(new_settings)


settings = SettingsObject()
_search_types = None


def get_search_types():
    """Creates and returns a dictionary of search type classes
    with the name/class as k/v pairs.

    :returns:  A dictionary of search type classes.
    """
    if not _search_types:
        global _search_types
        _search_types = {
            search_type.get_type_name(): search_type
            for search_type in [
                klass if inspect.isclass(klass) else getattr(
                    importlib.import_module(module),
                    klass
                )
                for module, klass in [
                    (None, st) if inspect.isclass(st) else st.rsplit('.', 1)
                    for st in getattr(
                        settings,
                        'ELASTICSEARCH_TYPE_CLASSES',
                        []
                    )
                ]
            ]
        }

    return _search_types
