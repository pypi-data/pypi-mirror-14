

Libres is a python library to reserve stuff:
`Libres on Github <https://github.com/seantis/libres/>`_

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Libres follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Libres uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.libres.png
  :target: https://travis-ci.org/OneGov/onegov.libres
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.libres/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.libres?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.libres/badge.png
  :target: https://crate.io/packages/onegov.libres
  :alt: Latest PyPI Release

License
-------
onegov.libres is released under GPLv2

Changelog
---------

0.1.2 (2016-04-06)
~~~~~~~~~~~~~~~~~~~

- Adds compatibility with Morepath 0.13.
  [href]

0.1.1 (2016-01-28)
~~~~~~~~~~~~~~~~~~~

- Uses the latest onegov.core release to get rid of some code.
  [href]

0.1.0 (2015-10-12)
~~~~~~~~~~~~~~~~~~~

- Removes Python 2.x support.
  [href]

0.0.6 (2015-08-28)
~~~~~~~~~~~~~~~~~~~

- The form definition field no longer requires an e-mail address.
  [href]

0.0.5 (2015-08-26)
~~~~~~~~~~~~~~~~~~~

- Adds a form definition field to the resource model.
  [href]

0.0.4 (2015-08-20)
~~~~~~~~~~~~~~~~~~~

- Adds an allocation highlight function to the resource. Apps can use this for
  easy Morepath Path/UI integration.
  [href]

- Adds a convenience function to get the scheduler by resource id.
  [href]

0.0.3 (2015-08-05)
~~~~~~~~~~~~~~~~~~~

- Removes first/last hour setting.
  [href]

0.0.2 (2015-08-05)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to only delete if there are no reservations.
  [href]

0.0.1 (2015-08-03)
~~~~~~~~~~~~~~~~~~~

- Initial Release


