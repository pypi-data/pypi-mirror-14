Middlebury Directory
====================

.. image:: https://travis-ci.org/coursereviews/directory.svg?branch=master
    :target: https://travis-ci.org/coursereviews/directory

A Python API for the Middlebury directory.

.. code-block:: python

    from directory import search

    search(email="dsilver@middlebury.edu")
    # [<Person 30972781062F9A6167A8D944F82CFD64>]

Simple Search
-------------

Perform a simple keyword search.

.. code-block:: python

    from directory import search

    search("Dana Silver")
    # [<Person 30972781062F9A6167A8D944F82CFD64>]

This is equivalent passing the ``query`` keyword argument:

.. code-block:: python

    from directory import search

    search(query="Dana Silver")
    # [<Person 30972781062F9A6167A8D944F82CFD64>]


Advanced Search
---------------

Perform an advanced search with some or all of the available search fields:
first_name, last_name, email, phone, address, location, job_title, person_type,
department.

You can't perform a simple search and an advanced search in the same query.
Setting `query` and any of the other fields will fail validation.

.. code-block:: python

    from directory import search

    search(email="dsilver@middlebury.edu")
    # [<Person 30972781062F9A6167A8D944F82CFD64>]

.. code-block:: python

    from directory import search

    search(first_name="Dana", person_type="Faculty")
    # [<Person 90338E439DA4652A2BDE2AC3F327A563>]


Advanced Usage
--------------

For raw access to validation and search fields, and control over when the HTTP
requests are sent, use the Search class. The Search class can be initialized
with any of the arguments to the search method.

.. code-block:: python

    from directory import Search

    # Construct a search object
    query = Search('Dana Silver')

    # Validate the search
    query.validate()

    # Get the search fields (makes an HTTP request for form parameters)
    query.search_fields()

    # Get the search results (makes HTTP requests for the search results)
    query.results()
