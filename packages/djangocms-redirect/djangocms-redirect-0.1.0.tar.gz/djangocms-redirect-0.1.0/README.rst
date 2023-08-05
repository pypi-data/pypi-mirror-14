=============================
djangocms-redirect
=============================

.. image:: https://img.shields.io/pypi/v/djangocms-redirect.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-redirect
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-redirect.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-redirect
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-redirect.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-redirect
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-redirect.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-redirect
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-redirect/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-redirect?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-redirect/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-redirect
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-redirect/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-redirect
   :alt: Code Climate


A django CMS enabled application to handle redirects

This is heavily borrowed from ``django.contrib.redirects`` with three major changes:

* Selection of django CMS pages
* Selection of redirect status code
* Middleware can processed in the request or response phase

Why using process_request?
--------------------------

Doing database queries in the middleware ``process_request`` is heavily discouraged as it's a
performance hit, especially when doing redirects which are just a tiny part of the
processed requests.
Except that sometimes it's just what you need (for example to "hide" content without deleting
/ unpublishing it)
By caching both existing and non existing redirects for a given URL the performance hit is
minimized for the use cases that requires ``process_request``.

Documentation
-------------

The full documentation is at https://djangocms-redirect.readthedocs.org.

Installation
------------

See https://djangocms-redirect.readthedocs.org/en/latest/installation.html

Features
--------

* Set old and new path, by selection existing django CMS pages or writing down the complete address
* Select the redirect status code (301, 302)
* Support for status code 410

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python setup.py test

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage-helper`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage-helper`: https://github.com/nephila/cookiecutter-djangopackage-helper
