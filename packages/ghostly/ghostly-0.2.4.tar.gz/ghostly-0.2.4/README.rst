=======
Ghostly
=======

Lightweight API around Selenium Webdriver and helpers for end to end testing
with Django.

This package is alpha, the API will most likely change!

It supports Django 1.6-1.8 for Python versions 2.7, 3.3, 3.4, 3.5 and pypy (where
the `Django version supports said Python version <https://docs.djangoproject.com/en/1.9/faq/install/#what-python-version-can-i-use-with-django>`_).

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

Docs
----

Available at `ghostly.readthedocs.org`_


Installation
------------

You can install ghostly either via the Python Package Index (PyPI) or from
github.

To install using pip;

.. code-block:: bash

    pip install ghostly

From github;

.. code-block:: bash

    $ pip install git+https://github.com/alexhayes/ghostly.git


Usage
-----

You can use use this package outside of Django however it has limited use.

Essentially there are two components, as follows;

- ``Ghostly`` - A lightweight wrapper and helper methods for Selenium
  Webdriver. Presently it provides a handful of methods that utilise xpath to
  deal with a page, such as ``xpath``, ``xpath_wait`` et al.
- ``GhostlyDjangoTestCase`` - A lightweight test case that extends
  `StaticLiveServerTestCase`_ and sets up an instance of ``Ghostly``. It
  provides methods such as ``assertCurrentUrl``, ``assertXpathEqual`` et al.

GhostlyDjangoTestCase
---------------------

``GhostlyDjangoTestCase`` inherits `StaticLiveServerTestCase`_ and thus fires up
a WSGI server that handles requests.

Given you have a named URL ``home`` with a ``<h1>Hello World</h1>`` visible in
the source, you can do the following;

.. code-block:: python

    class MyTestCase(GhostlyDjangoTestCase):

        def test_homepage(self):
            self.goto(reverse('home'))

            # Assert that an element is equal to something
            self.assertXpathEqual('//h1', 'Hello World')

            # Assert the current url, relative or absolute
            self.assertCurrentUrl('/home')


Working with SVG
----------------

To traverse SVG with Selenium web driver you must use xpath.

.. code-block:: python

    class MyTestCase(GhostlyDjangoTestCase):

        def test_homepage(self):
            self.goto(reverse('home'))

            # Click on an element, or example, in an SVG.
            self.ghostly.xpath_click('//*[@id="refresh"]')

            # Assert that an Xpath is equal to something
            self.assertXpathEqual('//h2', 'Hello World')

            # Wait for xpath to exist
            self.ghostly.xpath_wait('//div[@id="something"]')


History
-------

This package started out as a simple way to construct browser tests using YAML,
written by Brenton Cleeland.

The focus of this fork is to allow the developer to write programmatic unit
tests in the style of `unittest`_.

Currently this fork does not contain any of the CSS selector style methods that
were originally available as the focus has been on xpath only support until a
more robust CSS selector toolkit can be provided.


License
-------

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.


Author
------

- Alex Hayes <alex@commoncode.com>
- Brenton Cleeland <brenton@commoncode.com>

.. _StaticLiveServerTestCase: https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
.. _unittest: https://docs.python.org/2/library/unittest.html
.. _ghostly.readthedocs.org: http://ghostly.readthedocs.org/en/latest/
