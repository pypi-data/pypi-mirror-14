.. image:: https://img.shields.io/pypi/v/geokey-geotagx.svg
    :alt: PyPI Package
    :target: https://pypi.python.org/pypi/geokey-geotagx

.. image:: https://img.shields.io/travis/ExCiteS/geokey-geotagx/master.svg
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/ExCiteS/geokey-geotagx

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-geotagx/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-geotagx

geokey-geotagx
==============

Import results from `GeoTag-X <http://geotagx.org>`_.

Install
-------

geokey-geotagx requires:

- Python version 2.7
- GeoKey versions 0.9, 0.10, or 1.0

Install the extension from PyPI:

.. code-block:: console

    pip install geokey-geotagx

Or from cloned repository:

.. code-block:: console

    cd geokey-geotagx
    pip install -e .

Add the package to installed apps:

.. code-block:: console

    INSTALLED_APPS += (
        ...
        'geokey_geotagx',
    )

You're now ready to go!

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_geotagx

Check code coverage:

.. code-block:: console

    coverage run --source=geokey_geotagx manage.py test geokey_geotagx
    coverage report -m --omit=*/tests/*,*/migrations/*

API
---

To import results POST a feature collection:

.. code-block:: console

    POST /api/geotagx/:project_id/import/
    Content-Type: application/json

    {
        "type": "FeatureCollection",
        "features": []
    }

Returns (if successful):

.. code-block:: console

    HTTP/1.1 201 Created

    Objects created
