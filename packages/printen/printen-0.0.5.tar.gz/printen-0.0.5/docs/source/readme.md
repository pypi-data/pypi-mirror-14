Printen
=======

Printen is the a simple, flexible module for integrating
Elasticsearch into Python projects - especially projects
utilizing Peewee or Django models.

Printen's code is currently in active development and
should be considered alpha - breaking changes should
be expected.

Why Printen?
------------

There is no shortage of fine search libraries for Python.
The common tool used is [Haystack](http://haystacksearch.org/),
though this is oriented specifically towards Django, but
supports a multitude of search backends. This is a great
choice if you need flexibility in your search backends,
but one can begin to feel constrained as the interface to
the search backend is necessarily generic, so as to support
all search backends similarly.

Other options include [django-simple-elasticsearch](https://github.com/jaddison/django-simple-elasticsearch),
which has the advantage of specifically focusing on
Elasticsearch, but is limited to Django and isn't
under active development.

A final option is to use the excellent official
[Python Elasticsearch Client](http://elasticsearch-py.readthedocs.org/en/master/index.html),
which is not super hard, but does require a decent amount of work
to map it to the concepts of your ORM.

Printen seeks to do this work for you, without being overly
choosy about what Python framework you use it with (essentially
the opposite of Haystack - choosy about the search engine, not
choosy about the Python framework).

Elasticsearch Compatibility
---------------------------

Printen is expected to be compatible with Elasticsearch 2.0
and above.

Documentation
-------------

To see the complete documentation, visit Printen's documentation on [Read The Docs](http://printen.readthedocs.org/).

Installation
------------

Printen can still be intalled via pip:

    $ pip install printen

or if you have the source locally:

    $ python setup.py install

License
-------

Printen is licensed under the [BSD License](LICENSE.md)

Thanks
------

This was inspired by [James Addison's](https://github.com/jaddison)
[django-simple-elasticsearch](https://github.com/jaddison/django-simple-elasticsearch).
