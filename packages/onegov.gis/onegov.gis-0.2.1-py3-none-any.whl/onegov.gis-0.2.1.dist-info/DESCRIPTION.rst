

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Gis follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Gis uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.gis.png
  :target: https://travis-ci.org/OneGov/onegov.gis
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.gis/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.gis?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.gis.svg
    :target: https://badge.fury.io/py/onegov.gis
    :alt: Latest PyPI Release

License
-------
onegov.gis is released under GPLv2

Changelog
---------

0.2.1 (2016-04-06)
~~~~~~~~~~~~~~~~~~~

- Adds compatibility with Morepath 0.13.
  [href]

0.2.0 (2016-04-05)
~~~~~~~~~~~~~~~~~~~

- Changes the mouse pointer to default on unclickable markers.
  [href]

- Fixes form submit not working with enter key in map enabled forms.
  [href]

- Acquires the default view parameters from the body.
  [href]

0.1.0 (2016-04-05)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to display a (readonly) map with a marker.
  [href]

0.0.1 (2016-04-01)
~~~~~~~~~~~~~~~~~~~

- Initial Release


