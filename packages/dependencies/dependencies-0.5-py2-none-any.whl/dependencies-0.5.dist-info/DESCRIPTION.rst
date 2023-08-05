.. |travis| image:: https://img.shields.io/travis/proofit404/dependencies.svg?style=flat-square
    :target: https://travis-ci.org/proofit404/dependencies
    :alt: Build Status

.. |coveralls| image:: https://img.shields.io/coveralls/proofit404/dependencies.svg?style=flat-square
    :target: https://coveralls.io/r/proofit404/dependencies
    :alt: Coverage Status

.. |requires| image:: https://img.shields.io/requires/github/proofit404/dependencies.svg?style=flat-square
    :target: https://requires.io/github/proofit404/dependencies/requirements
    :alt: Requirements Status

.. |codacy| image:: https://img.shields.io/codacy/907efcab21d14e9ea1d110411d5791cd.svg?style=flat-square
    :target: https://www.codacy.com/app/proofit404/dependencies
    :alt: Code Quality Status

.. |pypi| image:: https://img.shields.io/pypi/v/dependencies.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dependencies/
    :alt: Python Package Version

============
Dependencies
============

|travis| |coveralls| |requires| |codacy| |pypi|

Dependency Injection for Humans.

- `Source Code`_
- `Issue Tracker`_

Installation
------------

All released versions are hosted on the Python Package Index.  You can
install this package with following command.

.. code:: bash

    pip install dependencies

License
-------

Dependencies library is offered under LGPL license.

.. _source code: https://github.com/proofit404/dependencies
.. _issue tracker: https://github.com/proofit404/dependencies/issues

.. :changelog:

Changelog
---------

0.5 (2016-03-03)
++++++++++++++++

- Avoid attribute search recursion.  This occurs with inheritance
  chain length started at 3 and missing dependency on first level.
- Add ``c`` alias for ``Injector`` subclass access.
- Add ``let`` factory to temporarily overwrite specified
  dependencies.

0.4 (2016-03-03)
++++++++++++++++

- Detect ``object.__init__`` and skip it in the argument injection.

0.3 (2016-03-02)
++++++++++++++++

- Deprecate injectable mechanism.  Injector may inject any arguments
  to any classes.  Injector now support multiple DI targets.  All
  possible targets now specified in the Injector attributes.  Only
  single base inheritance allowed for Injector subclasses.

0.2 (2016-02-13)
++++++++++++++++

- Allows to override dependencies specified with Injector by
  inheritance from this Injector subclass.

0.1 (2016-01-31)
++++++++++++++++

- Initial release.


