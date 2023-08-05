.. image:: https://img.shields.io/travis/ExCiteS/geokey-webresources/master.svg
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/ExCiteS/geokey-webresources

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-webresources/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-webresources

geokey-webresources
===================

Extend GeoKey projects by adding web resources: GeoJSON, KML or GPX.

Install
-------

geokey-webresources requires:

- Python version 2.7
- GeoKey version 0.9 or greater

Install the geokey-webresources from PyPI:

.. code-block:: console

    pip install geokey-webresources

Or from cloned repository:

.. code-block:: console

    cd geokey-webresources
    pip install -e .

Add the package to installed apps:

.. code-block:: console

    INSTALLED_APPS += (
        ...
        'geokey_webresources',
    )

Migrate the models into the database:

.. code-block:: console

    python manage.py migrate geokey_webresources

You're now ready to go!

Update
------

Update the geokey-webresources from PyPI:

.. code-block:: console

    pip install -U geokey-webresources

Migrate the new models into the database:

.. code-block:: console

    python manage.py migrate geokey_webresources

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_webresources

Check code coverage:

.. code-block:: console

    pip install coverage
    coverage run --source=geokey_webresources manage.py test geokey_webresources
    coverage report -m --omit=*/tests/*,*/migrations/*

Public API
----------

**Get all web resources of a project**

.. code-block:: console

    GET /api/projects/:project_id/webresources/

*Request parameters:*

==========  ======= ====================================
Parameter   Type    Description
==========  ======= ====================================
project_id  Integer A unique identifier for the project.
==========  ======= ====================================

*Response:*

The response contains an array of web resources. If the array is empty, then the project has no active web resources.

.. code-block:: console

    [
        {
            "id": 46,
            "status": "active",
            "name": "Public Houses",
            "description": "All public houses in London.",
            "created": "2014-09-19T15:51:32.790Z",
            "modified": "2014-09-21T15:51:32.804Z",
            "data_format": "KML",
            "url": "http://london.co.uk/public-houses.kml",
            "colour": "#000000",
            "symbol": null
        }
    ]

*Response status codes:*

==== ========================================================
Code Reason
==== ========================================================
200  The list of projects has been returned successfully.
404  The project was not found (or user has no access to it).
==== ========================================================

**Get a single web resource of a project**

.. code-block:: console

    GET /api/projects/:project_id/webresources/:webresource_id/

*Request parameters:*

==============  ======= =========================================
Parameter       Type    Description
==============  ======= =========================================
project_id      Integer A unique identifier for the project.
webresource_id  Integer A unique identifier for the web resource.
==============  ======= =========================================

*Response:*

.. code-block:: console

    {
        "id": 46,
        "status": "active",
        "name": "Train Stations",
        "description": "Train stations in Germany.",
        "created": "2015-09-15T09:40:01.747Z",
        "modified": "2016-01-10T07:12:01.827Z",
        "data_format": "GeoJSON",
        "url": "https://germany.de/all-train-stations.geojson",
        "colour": "#ffc0cb",
        "symbol": '/media/webresources/symbols/train_stations.png'
    }

*Response status codes:*

==== ====================================================
Code Reason
==== ====================================================
200  The list of projects has been returned successfully.
404  The project or web resource was not found.
==== ====================================================
