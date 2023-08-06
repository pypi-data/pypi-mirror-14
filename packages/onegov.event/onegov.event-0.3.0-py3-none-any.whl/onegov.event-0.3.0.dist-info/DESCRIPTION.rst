

Requirements
------------

This package requires the `HSTORE extension <http://www.postgresql.org/docs/9.4/static/hstore.html>`_

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Events follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Events uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.event.png
  :target: https://travis-ci.org/OneGov/onegov.event
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.event/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.event?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/onegov.event.svg
  :target: https://pypi.python.org/pypi/onegov.event
  :alt: Latest PyPI Release

License
-------
onegov.event is released under GPLv2

Changelog
---------

0.3.0 (2016-04-05)
~~~~~~~~~~~~~~~~~~~

- Adds onegov.gis coordinates to events.
  [href]

0.2.0 (2015-11-12)
~~~~~~~~~~~~~~~~~~~

- Adds CSV import and export.
  [msom]

0.1.0 (2015-10-12)
~~~~~~~~~~~~~~~~~~~

- Removes Python 2.x support.
  [href]

0.0.6 (2015-09-25)
~~~~~~~~~~~~~~~~~~~

- Adds onegov.search integration.
  [href]

0.0.5 (2015-09-15)
~~~~~~~~~~~~~~~~~~~

- Add an optional URL to ical exports.
  [msom]

- Cleanup the documentation.
  [msom]

0.0.4 (2015-09-08)
~~~~~~~~~~~~~~~~~~~

- Add cli command for guidle import (experimental).
  [msom]

- Add ical export functions.
  [msom]

0.0.3 (2015-09-03)
~~~~~~~~~~~~~~~~~~~

- Don't delete old event automatically.
  [msom]

0.0.2 (2015-08-28)
~~~~~~~~~~~~~~~~~~~

- Use hstore for tags.
  [msom]

- Filter for current occurrences by default.
  [msom]

- Add autoclean option to add event function.
  [msom]

- Add by_id method for event collections.
  [msom]

- Automatically remove old initiated events.
  [msom]

0.0.1 (2015-08-20)
~~~~~~~~~~~~~~~~~~~

- Initial Release


