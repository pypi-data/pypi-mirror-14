RC QueryBuilder: Fluent QueryBuilder for MongoDB
================================================

The **rcquerybuilder** package provides a fluent api wrapper around pymongo queries.

This allows you to write and execute mongodb queries like this:

.. code-block:: python

    >>> from rcquerybuilder.builder import Builder
    >>> qb = Builder(collection=None)
    >>> qb.field('name').equals('foobar') \
    ...   .field('fizz').ne(None) \
    ...   .get_query_list()
    {'name': 'foobar', 'fizz': {'$ne': None}}

Installation
------------

To install rcquerybuilder, simply:

.. code-block:: bash

    $ pip install rcquerybuilder

Documentation
-------------

Documentation is available at https://rcquerybuilder.readthedocs.org.

How to Contribute
-----------------

#. Fork `the repository`_ to start making your changes on the **master** branch (or branch off of it).
#. Send a pull request and make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/red-crown/mongo-querybuilder
.. _AUTHORS: https://github.com/red-crown/mongo-querybuilder/blob/master/AUTHORS.rst


