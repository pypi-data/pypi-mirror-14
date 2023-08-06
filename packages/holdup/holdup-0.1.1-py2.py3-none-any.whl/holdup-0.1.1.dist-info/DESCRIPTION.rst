========
Overview
========



A tool to wait for services and execute command. Useful for Docker containers that depend on slow to start services
(like almost everything).

* Free software: BSD license

Installation
============

::

    pip install holdup

Documentation
=============

Usage: ``holdup [-h] [-f] [-t SECONDS] [-n] [service [service ...]] [-- command [arg [arg ...]]]``

Wait for services to be ready and optionally exec command.

positional arguments:
  service               A service to wait for. Supported protocols: "tcp://host:port/", "unix:///path/to/domain.sock".
  command               An optional command to exec.

optional arguments:
  -h, --help            show this help message and exit
  -t SECONDS, --timeout SECONDS
                        Time to wait for services to be ready. Default: 5.0
  -n, --no-abort        Ignore failed services. This makes `holdup` return 0
                        exit code regardless of services actually responding.

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

0.1.0 (2016-04-21)
-----------------------------------------

* First release on PyPI.


