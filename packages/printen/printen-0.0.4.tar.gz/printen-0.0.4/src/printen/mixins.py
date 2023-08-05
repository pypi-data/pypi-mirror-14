import gc
from elasticsearch import Elasticsearch, TransportError
from .exceptions import MissingObjectError
import config


class ElasticsearchIndexMixin(object):
    """
    This class can be used with a standalone class or
    directly on your model. There are several methods
    that you are required to subclass in order to
    use this.
    """
    @classmethod
    def get_es(cls):
        """Returns the configured reference to the Elasticsearch
        instance.

        :returns:  The elasticsearch instance
        :raises: Misconfigured
        """
        if not hasattr(cls, '_es'):
            cls._es = Elasticsearch(**cls.get_es_connection_settings())
        return cls._es

    @classmethod
    def get_es_connection_settings(cls):
        """Returns the connection parameters for Elasticsearch

        :returns:  A dictionary containing key/value pairs of
                    connection parameters
        :raises: AttributeError
        """
        return config.settings.ELASTICSEARCH_CONNECTION_PARAMS

    @classmethod
    def get_index_name(cls):
        """Allows indexing code to know the name of the index to use.
        This defaults to `index` but can be overridden by setting
        the `ELASTICSEARCH_INDEX_NAME` in your configuration, or
        overriding this method on a per-model basis.

        :returns:  A string containing the index name.
        """
        return getattr(config.settings, 'ELASTICSEARCH_INDEX_NAME', 'index')

    @classmethod
    def get_type_name(cls):
        """This provides Elasticsearch with a name with which to
        do type mappings for your model. Defaults to
        cls.__class__.__name__.

        :returns:  A string naming the type of thing being indexed.
        """
        return cls.__name__

    @classmethod
    def get_document_id(cls, obj):
        """Returns the document id, which usually corresponds to
        the objects primary key in the database.

        You *must* override this method.

        :param obj: The object to derive an id from.
        :type obj: A python object which you are indexing.
        :returns:  An integer representing the document's id.
        """
        raise NotImplementedError

    @classmethod
    def get_document(cls, obj):
        """Returns the 'document' to be indexed, which is a dictionary
        representation of the object passed in, including the relevant
        fields you wish to be in the search engine.

        You *must* override this method.

        :param obj: The object to generate a document for.
        :type obj: A python object which you are indexing.
        :returns:  A dictionary with key/value pairs of fields and values.
        """
        raise NotImplementedError

    @classmethod
    def get_request_params(cls, obj):
        """Overridable per-model request parameters for
        Elasticsearch.

        :param obj: The object involved in the request.
        :type obj: A python object which you are indexing.
        :returns:  Request parameters dictionary passed to Elasticsearch's
                   index operation.
        """
        return {}

    @classmethod
    def get_type_mapping(cls):
        """Overridable per-model type mapping for
        Elasticsearch.

        :returns:  Type mapping for this type used when creating the index.
        """
        return {}

    @classmethod
    def get_queryset(cls):
        """Get a queryset for the model.

        You *must* implement this yourself.

        :returns:  An object with an interface that your queryset_iterator
                   method knows how to iterate over.
        """
        raise NotImplementedError

    @classmethod
    def queryset_iterator(cls, queryset):
        """Iterate (using a generator) over a given queryset.

        You *must* implement this yourself.

        :param queryset: The queryset to iterate over.
        :type queryset: A type which provides an interface this
                        method knows how to iterate over.
        :yields:        Instances of the object to index.
        """
        raise NotImplementedError

    @classmethod
    def get_bulk_index_batch_size(cls):
        """Get the number of items to limit bulk indexing to
        at a time (i.e. per call to the Elasticsearch server).

        Defaults to 100. Set `ELASTICSEARCH_BULK_INDEX_BATCH_SIZE`
        to change this value, or override this method.

        :returns:  An integer.
        """
        return getattr(
            config.settings,
            'ELASTICSEARCH_BULK_INDEX_BATCH_SIZE',
            100
        )

    @classmethod
    def should_index(cls, obj):
        """Determines if an obj should be indexed.

        Defaults to True

        :param obj: The object to generate a document for.
        :type obj: A python object which you are indexing.
        :returns:  A Boolean.
        """
        return True

    @classmethod
    def bulk_index(cls, index_name='', queryset=None):
        """Initiate a bulk index of all items returned
        by the queryset.

        :param index_name: The index to update. By default this
                           is the value returned by :func:`get_index_name`
        :param queryset: The queryset to iterate over.
        """
        es = cls.get_es()

        tmp = []

        if queryset is None:
            queryset = cls.get_queryset()

        for obj in cls.queryset_iterator(queryset):
            delete = not cls.should_index(obj)

            data = {
                '_index': index_name or cls.get_index_name(),
                '_type': cls.get_type_name(),
                '_id': cls.get_document_id(obj)
            }
            data.update(cls.get_request_params(obj))
            data = {'delete' if delete else 'index': data}
            tmp.append(data)

            if not delete:
                tmp.append(cls.get_document(obj))

            if not len(tmp) % cls.get_bulk_index_batch_size():
                es.bulk(tmp)
                tmp = []

        if tmp:
            es.bulk(tmp)

    @classmethod
    def index_add(cls, obj, index_name=None):
        """Adds a single object to the index.

        :param obj: The object to index.
        :type obj: A python object which you are indexing.
        :param index_name: The index to update. By default this
                           is the value returned by :func:`get_index_name`
        :returns:  A Boolean indicating if the object was added.
        """
        if obj and cls.should_index(obj):
            cls.get_es().index(
                index_name or cls.get_index_name(),
                cls.get_type_name(),
                cls.get_document(obj),
                cls.get_document_id(obj),
                **cls.get_request_params(obj)
            )
            return True
        return False

    @classmethod
    def index_delete(cls, obj, index_name=None):
        """Removes a single object to the index.

        :param obj: The object to index.
        :type obj: A python object which you are indexing.
        :param index_name: The index to update. By default this
                           is the value returned by :func:`get_index_name`
        :returns:  A Boolean indicating if the object was removed.
        """
        if obj:
            try:
                cls.get_es().delete(
                    index_name or cls.get_index_name(),
                    cls.get_type_name(),
                    cls.get_document_id(obj),
                    **cls.get_request_params(obj)
                )
            except TransportError as e:
                if e.status_code != 404:
                    raise
            return True
        return False

    @classmethod
    def index_add_or_delete(cls, obj, index_name=None):
        """Adds or removes an object depending on the return value
        of :func:`should_index`.

        :param obj: The object to index.
        :type obj: A python object which you are indexing.
        :param index_name: The index to update. By default this
                           is the value returned by :func:`get_index_name`
        :returns:  A Boolean indicating if the object was added/removed.
        """
        if obj:
            if cls.should_index(obj):
                return cls.index_add(obj, index_name)
            else:
                return cls.index_delete(obj, index_name)
        return False

    @classmethod
    def save_handler(cls, sender, instance):
        """A target for wiring to a save signal for your
        model.

        :param sender: The class which initated the save.
        :param instance: The instance being saved.
        """
        cls.index_add_or_delete(instance)

    @classmethod
    def delete_handler(cls, sender, instance, **kwargs):
        """A target for wiring to a delete signal for your
        model.

        :param sender: The class which initated the delete.
        :param instance: The instance being delete.
        """
        cls.index_delete(instance)


class PeeweeElasticsearchIndexMixin(ElasticsearchIndexMixin):
    """
    A class that inherits from ElasticsearchIndexMixin,
    overriding the relevant methods with Peewee related
    defaults.
    """
    @classmethod
    def get_type_name(cls):
        """Provides a sane default for Peewee models. Override
        to modify behavior.

        :returns: `cls.model._meta.name`
        """
        return cls.model._meta.name

    @classmethod
    def get_document_id(cls, obj):
        """Provides a sane default for Peewee models. Override
        to modify behavior.

        :param obj: The object to index.
        :type obj: A subclass of peewee.Model
        :returns: `getattr(obj, obj._meta.primary_key.name)` which is
                  an integer document id
        :raises: MissingObjectError
        """
        try:
            doc_id = getattr(obj, obj._meta.primary_key.name, None)
        except AttributeError:
            doc_id = None

        if not doc_id:
            raise MissingObjectError

        return doc_id

    @classmethod
    def get_queryset(cls):
        """Provides a sane default for Peewee models. Override
        to modify behavior.

        :returns: `cls.model.select()` - a Peewee queryset
        """
        return cls.model.select()

    @classmethod
    def queryset_iterator(cls, queryset):
        """Provides a sane default for Peewee models. Override
        to modify behavior.

        Executes the given queryset and iterates over the results,
        yielding them one at a time to the caller.

        :param queryset: A Peewee queryset to iterate over.
        :type queryset: A `Peewee queryset <http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery>`_.
        :returns: `cls.model.select()` - a Peewee queryset
        """
        for result in queryset.execute().iterator():
            yield result


class DjangoElasticsearchIndexMixin(ElasticsearchIndexMixin):
    """
    A class that inherits from ElasticsearchIndexMixin,
    overriding the relevant methods with Django related
    defaults.
    """
    @classmethod
    def get_type_name(cls):
        """Provides a sane default for Django models. Override
        to modify behavior.

        :returns: String with a dot separated app_label and model_name.
        """
        return '{}.{}'.format(cls._meta.app_label, cls._meta.model_name)

    @classmethod
    def get_document_id(cls, obj):
        """Provides a sane default for Django models. Override
        to modify behavior.

        :param obj: The object to index.
        :type obj: A subclass of `django.db.models.Model <https://docs.djangoproject.com/en/1.9/ref/models/instances/#django.db.models.Model>`_.
        :returns: `obj.pk`, an integer.
        :raises: MissingObjectError
        """
        if not obj:
            raise MissingObjectError

        try:
            doc_id = obj.pk
        except AttributeError:
            doc_id = None

        if not doc_id:
            raise MissingObjectError

        return obj.pk

    @classmethod
    def get_queryset(cls):
        """Provides a sane default for Django models. Override
        to modify behavior.

        :returns: A `Django QuerySet <https://docs.djangoproject.com/en/1.9/ref/models/querysets/>`_..
        """
        return cls.objects.all()

    def queryset_iterator(self, queryset, chunksize=1000):
        """Provides a sane default for Django models. Override
        to modify behavior.

        :param queryset: A Django QuerySet to iterate over.
        :type queryset: A `Django QuerySet <https://docs.djangoproject.com/en/1.9/ref/models/querysets/>`_.
        :returns: An instance of our model object.
        """
        try:
            last_pk = queryset.order_by('-pk')[0].pk
        except IndexError:
            return

        queryset = queryset.order_by('pk')
        pk = queryset[0].pk - 1
        while pk < last_pk:
            for row in queryset.filter(pk__gt=pk)[:chunksize]:
                pk = row.pk
                yield row
            gc.collect()
