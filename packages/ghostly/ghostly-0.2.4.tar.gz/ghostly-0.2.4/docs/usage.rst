=====
Usage
=====

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


.. _StaticLiveServerTestCase: https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
.. _unittest: https://docs.python.org/2/library/unittest.html
