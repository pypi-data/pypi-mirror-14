"""
This contains all external calls to the Elasticsearch client
in a handy single location
"""

from elasticsearch import Elasticsearch
import config


def get_aliases():
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    return es.indices.get_aliases()


def get_settings(index_name):
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    return es.indices.get_settings(index_name)


def update_aliases(actions):
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    es.indices.update_aliases(actions)


def create_index(index_name, index_settings):
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    es.indices.create(index_name, index_settings)


def delete_indices(indices=None):
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    if not indices:
        indices = []

    for index in indices:
        if es.indices.exists(index):
            es.indices.delete(index)


def refresh_index(index_name):
    es = Elasticsearch(**config.settings.ELASTICSEARCH_CONNECTION_PARAMS)

    es.indices.refresh(index_name)
