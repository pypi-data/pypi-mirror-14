.. image:: https://img.shields.io/pypi/v/geokey-export.svg
    :alt: PyPI Package
    :target: https://pypi.python.org/pypi/geokey-export

.. image:: https://img.shields.io/travis/ExCiteS/geokey-export/master.svg
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/ExCiteS/geokey-export

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-export/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-export

geokey-export
=============

Export data from GeoKey into various formats.

Currently supported formats:

- KML
- GeoJSON

Install
-------

geokey-export requires:

- Python version 2.7
- GeoKey version 1.0

Install the extension from PyPI:

.. code-block:: console

    pip install geokey-export

Or from cloned repository:

.. code-block:: console

    cd geokey-export
    pip install -e .

Add the package to installed apps:

.. code-block:: python

    INSTALLED_APPS += (
        ...
        'geokey_export',
    )

Migrate the models into the database:

.. code-block:: console

    python manage.py migrate geokey_export

Copy static files:

.. code-block:: console

    python manage.py collectstatic

You're now ready to go!

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_export

Check code coverage:

.. code-block:: console

    coverage run --source=geokey_export manage.py test geokey_export
    coverage report -m --omit=*/tests/*,*/migrations/*
