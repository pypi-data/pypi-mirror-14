Usage
-----

Integrating Printen into your poject is quite easy. First, we assume
that you have an Elasticsearch server set up, and that your project
makes use of some sort of simple model-based ORM or similar setup.


Creating Search Types
=====================

The main currency of Printen is a search type class. Basically this
maps to [Elasitcsearch Mapping Types](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-type).
Most typically, these correspond one to one with your model classes
and creating one is as simple as dropping in the
[ElasticsearchIndexMixin](/api.html#printen.mixins.ElasticsearchIndexMixin)
into a class declaration. This class can either be the model itself
or a dedicated class for search.

As an example, we'll create a dedicated search class,
using Peewee as our ORM:

    from printen.mixins import PeeweeElasticsearchIndexMixin
    import models

    class BlogPostSearch(PeeweeElasticsearchIndexMixin):
        model = models.BlogPost

        @classmethod
        def get_document(cls, obj):
            return {
                'id': obj.id,
                'title': obj.title,
                'content': obj.content,
                'tags': obj.tags,
                'author': obj.author
            }

Pretty simple, huh? All you need to do is tell the class
what model it will indexing by setting the model attribute,
in this case to models.BlogPost. Then override the
get_document method, so that you can specify what fields you
want indexed. The obj passed in here is just an instance of
models.BlogPost - the model you specified. Return a dictionary
where each key is a field in the Elasitcsearch document. Once
you also tell the class what model it uses (in this case
models.BlogPost) you are all set. If you are using Peewee
(or Django, in which case you simply use the
DjangoElasticsearchIndexMixin) you can skip to the next
section.

The Peewee and Django versions of the ElasticsearchIndexMixin
handle a few things for us that the regular
ElasticsearchIndexMixin does not. If you are using another ORM,
or some other sort of persistence for your data, it's not too
hard to use the ElasticsearchIndexMixin directly:

    from printen.mixins import ElasticsearchIndexMixin
    import models

    class BlogPostSearch(ElasticsearchIndexMixin):
        model = models.BlogPost

        @classmethod
        def get_document(cls, obj):
            return {
                'id': obj.id,
                'title': obj.title,
                'content': obj.content,
                'tags': obj.tags,
                'author': obj.author
            }

        @classmethod
        def get_document_id(cls, obj):
            return obj.id

        @classmethod
        def get_queryset(cls):
            return cls.queryset

        @classmethod
        def queryset_iterator(cls, queryset):
            for result in queryset:
                yield result

The model attribute and get_document method should be familiar
to you - our assumption here is that regardless of what the
actual storage layer is, the obj that gets passed in
(which will be an instance of the class pointed to by the model
attribute) has some information that you will map to fields
to be returned to the Elasticsearch indexing process. A couple
more methods are necessary in this case though.

The get_document_id needs to return some sort of unique identifier
for your object. Often that's simply obj.id, but you can make it
whatever you want.

The get_queryset method is used to retrieve an iterable object
which is used to retrieve multiple instances of your model.
This can be a powerful way to filter out instances you may
not want indexed for some reason. Both Django and Peewee
offer powerful QuerySet classes - perhaps your other ORM
or persistence layer does as well, or you can create a
simple method yourself.

Finally, the queryset_iterator handles iterating on
the queryset, in this case yielding rows one by one.

Configuration
=============

Now that you have your search type mapping classes set up, you
need to tell Printen to use them as well as let it know about
where your Elasticsearch server is and configure other
settings. Configuring Printen is easy:

    from printen.config import configure

    configure({
        'ELASTICSEARCH_DELETE_OLD_INDICES': True,
        'ELASTICSEARCH_INDEX_NAME': 'example',
        'ELASTICSEARCH_TYPE_CLASSES': [
            'app.search.BlogPost',
            'app.search.Comment'
        ],
        'ELASTICSEARCH_CONNECTION_PARAMS': {
            'hosts': 'http://127.0.0.1:9200',
        },
    })

If using Flask, a good place to put this is after your app
configuration is loaded:

    configure(app.config['ELASTICSEARCH_SETTINGS'])

Where we assume that ELASTICSEARCH_SETTINGS in your config
returns a dictionary similar in structure to the above.

Let's walk through the various settings.

* ELASTICSEARCH_DELETE_OLD_INDICES: This controls whether old indices will be
deleted when bulk reindexing. You usually want this set to True.
* ELASTICSEARCH_INDEX_NAME: The default index name. Can be overriden per-model
using the [get_index_name](/api.html#printen.mixins.ElasticsearchIndexMixin.get_index_name)
method.
* ELASTICSEARCH_TYPE_CLASSES: A list of strings or classes enumerating the
classes you created in [Creating Search Types](#Creating Search Types)
* ELASTICSEARCH_CONNECTION_PARAMS: The kwargs to pass to the instatiation of
the [Elasticsearch](http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch)
object. The only required argument is 'hosts' (note the plural).

Building Your Index
===================

Building your indices is pretty straight forward. If you were using Flask,
for example, you could just do the following in a manage.py:

    from flask.ext.script import Manager
    from printen.utils import rebuild_indices, delete_indices

    @manager.command
    def drop_search_indices(indices):
        indices = indices.split(',')
        delete_indices(indices)

    @manager.command
    def rebuild_indices():
        rebuild_indices()

    if __name__ == "__main__":
        manager.run()

Now to do a bulk index of all your model data:

    $ python manage.py rebuild_indices

That's it. Your data is now in Elasticsearch.

For removing your indices entirely (as opposed to updating
data by calling the rebuild_indices command or by responding
to signals as is discussed below), you can call the
`drop_search_indices` command along with the name of the
index or indices you want to drop:

    $ python manage.py drop_search_indices myindex

If you have multiple indices, you can separate them by
commas.


Querying Your Index
===================

Querying your index is largely handled by you directly, but it's quite
easy using the Elasticsearch module, which Printen depends already
anyway. Here's an example endpoint you could have in a Flask
endpoint.

    import printen.config

    @app.route('/api/search/', methods=['GET'])
    def search():
        if request.method == 'GET':
            request_data = request.args
        else:
            raise NotImplementedError('{} not supported!'.format(request.method))

        query = request_data.get('query')
        search_types = printen.config.get_search_types()
        search_type = search_types.get(request_data.get('search_type'))

        if not search_type:
            return ''

        if query:
            query_dict = {
                'simple_query_string': {
                    'query': query
                }
            }
        else:
            query_dict = {
                'match_all': {}
            }

        es = search_type.get_es()
        return json.dumps(es.search(
            index=search_type.get_index_name(),
            doc_type=search_type.model._meta.name,
            body={
                'query': query_dict
            }
        ), indent=4, separators=(',', ': '))

Reviewing this a bit, the endpoint expects a GET call with a query
and search_type. We retrieve our search_types from printen, which
allows us to retrieve the search_type object. If we were given a
query, we use a [simple_query_string](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-simple-query-string-query.html),
otherwise we use an empty [match_all](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html).
Afterwards, we package this all up together in a call to
[Elasticsearch.search](http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch.search)
and dump the return to json to be consumed by the requesting client.

Responding to Changes in Data
=============================

This covers most of the basics of implementing Printen, but one
important aspect to a smoothly running search service is the
ability to respond immediately to changes to your data. The key
to this is making use of your ORM's signaling facilities
([Django Signals](https://docs.djangoproject.com/en/1.9/topics/signals/)
or [Peewee Signals](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#signals))
to reindex an individual instance when it is created, modified,
or deleted. An example using Peewee:

    import playhouse.signals
    import models

    playhouse.signals.post_save.connect(
        BlogPostSearch.save_handler,
        'BlogPostSave',
        sender=models.BlogPost
    )
    playhouse.signals.post_delete.connect(
        BlogPostSearch.delete_handler,
        'BlogPostDelete',
        sender=models.BlogPost
    )

This ensures that changes to your models are reflected immediately
in the search index, but it has the problem that the default
implementation of save_handler and delete_handler immediately,
within the calling process, initiate these changes. A better
method is to override them to make use of Celery workers or
Amazon's Lambda service so that they occur outside of your main
web process.
