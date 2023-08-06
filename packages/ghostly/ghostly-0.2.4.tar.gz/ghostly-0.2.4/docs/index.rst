=======
ghostly
=======

Lightweight API around Selenium Webdriver and helpers for end to end testing
with Django.

This package is alpha, the API will most likely change!

It supports Django 1.6+ for Python versions 2.7, 3.3, 3.4, 3.5 and pypy (where
the Django version supports the Python version).

.. image:: https://travis-ci.org/alexhayes/ghostly.png?branch=master
    :target: https://travis-ci.org/alexhayes/ghostly
    :alt: Build Status

.. image:: https://landscape.io/github/alexhayes/ghostly/master/landscape.png
    :target: https://landscape.io/github/alexhayes/ghostly/
    :alt: Code Health

.. image:: https://codecov.io/github/alexhayes/ghostly/coverage.svg?branch=master
    :target: https://codecov.io/github/alexhayes/ghostly?branch=master
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/ghostly/badge/
    :target: http://ghostly.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/ghostly.svg
    :target: https://pypi.python.org/pypi/ghostly
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/ghostly.svg
    :target: https://pypi.python.org/pypi/ghostly/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/dd/ghostly.svg
    :target: https://pypi.python.org/pypi/ghostly/
    :alt: Downloads


Contents
--------

.. toctree::
 :maxdepth: 1

 installation
 usage
 developer
 internals/reference/index

License
-------

This software is licensed under the `MIT License`. See the `LICENSE`_.


History
-------

This package started out as a simple way to construct browser tests using YAML,
written by Brenton Cleeland.

The focus of this fork is to allow the developer to write programmatic unit
tests in the style of `unittest`_.

Currently this fork does not contain any of the CSS selector style methods that
were originally available as the focus has been on xpath only support until a
more robust CSS selector toolkit can be provided.


Author
------

- Alex Hayes <alex@commoncode.com>
- Brenton Cleeland <brenton@commoncode.com>


.. _StaticLiveServerTestCase: https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
.. _unittest: https://docs.python.org/2/library/unittest.html
.. _LICENSE: https://github.com/alexhayes/ghostly/blob/master/LICENSE
