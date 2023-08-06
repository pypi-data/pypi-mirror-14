.. image:: https://img.shields.io/pypi/v/geokey-cartodb.svg
    :alt: PyPI Package
    :target: https://pypi.python.org/pypi/geokey-cartodb

.. image:: https://img.shields.io/travis/ExCiteS/geokey-cartodb/master.svg
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/ExCiteS/geokey-cartodb

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-cartodb/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-cartodb

geokey-cartodb
==============

Provide API endpoints that can be used to import GeoKey data into CartoDB.

Install
-------

geokey-cartodb requires:

- Python version 2.7
- GeoKey versions 0.9, 0.10, or 1.0

Install the extension from PyPI:

.. code-block:: console

    pip install geokey-cartodb

Or from cloned repository:

.. code-block:: console

    cd geokey-cartodb
    pip install -e .

Add the package to installed apps:

.. code-block:: console

    INSTALLED_APPS += (
        ...
        'geokey_cartodb',
    )

Migrate the models into the database:

.. code-block:: console

    python manage.py migrate geokey_cartodb

You're now ready to go!

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_cartodb

Check code coverage:

.. code-block:: console

    coverage run --source=geokey_cartodb manage.py test geokey_cartodb
    coverage report -m --omit=*/tests/*,*/migrations/*
