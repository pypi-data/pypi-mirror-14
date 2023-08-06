========
Overview
========



A simple configurator helper to help you to magically configure your repository to publich the content in a doc file to
gh-pages using sphinx.

* Free software: BSD license

Installation
============

::

    pip install vxghpages

Documentation
=============

https://vxghpages.readthedocs.org/

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


Changelog
=========

0.1.0 (2016-04-11)
-----------------------------------------

* First release on PyPI.


