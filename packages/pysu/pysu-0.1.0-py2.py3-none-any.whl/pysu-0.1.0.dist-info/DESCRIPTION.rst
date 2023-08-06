========
Overview
========



Simple Python-based setuid+setgid+setgroups+exec. A port of https://github.com/tianon/gosu

* Free software: BSD license

Installation
============

::

    pip install pysu

Documentation
=============

https://python-su.readthedocs.org/

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

0.1.0 (2016-04-19)
-----------------------------------------

* First release on PyPI.


