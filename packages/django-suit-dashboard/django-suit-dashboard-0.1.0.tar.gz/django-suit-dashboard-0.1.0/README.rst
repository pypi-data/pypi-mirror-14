========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
        | |landscape|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/django-suit-dashboard/badge/?version=latest
    :target: https://django-suit-dashboard.readthedocs.org/en/latest/
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Pawamoy/django-suit-dashboard.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Pawamoy/django-suit-dashboard

.. |codecov| image:: https://codecov.io/github/Pawamoy/django-suit-dashboard/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Pawamoy/django-suit-dashboard

.. |landscape| image:: https://landscape.io/github/Pawamoy/django-suit-dashboard/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Pawamoy/django-suit-dashboard/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/django-suit-dashboard.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/django-suit-dashboard

.. |downloads| image:: https://img.shields.io/pypi/dm/django-suit-dashboard.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/django-suit-dashboard

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-suit-dashboard.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/django-suit-dashboard

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/django-suit-dashboard.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/django-suit-dashboard

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/django-suit-dashboard.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/django-suit-dashboard


.. end-badges

Create a dashboard within django-suit admin interface

License
=======

Software licensed under `MPL 2.0`_ license.

.. _BSD-2 : https://opensource.org/licenses/BSD-2-Clause
.. _MPL 2.0 : https://www.mozilla.org/en-US/MPL/2.0/

Installation
============

::

    pip install django-suit-dashboard

Documentation
=============

https://django-suit-dashboard.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
