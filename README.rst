========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-duo/badge/?style=flat
    :target: https://readthedocs.org/projects/python-duo
    :alt: Documentation Status


.. |version| image:: https://img.shields.io/pypi/v/duo.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/duo

.. |commits-since| image:: https://img.shields.io/github/commits-since/enningb/python-duo/v0.1.3.svg
    :alt: Commits since latest release
    :target: https://github.com/enningb/python-duo/compare/v0.1.3...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/duo.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/duo

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/duo.svg
    :alt: Supported versions
    :target: https://pypi.org/project/duo

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/duo.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/duo


.. end-badges

A package that extracts data from Dienst Uitvoering Onderwijs.

* Free software: MIT license

Installation
============

::

    pip install duo

Documentation
=============


https://python-duo.readthedocs.io/


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
