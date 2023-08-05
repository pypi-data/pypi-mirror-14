===================
djangocms-page-meta
===================

.. image:: https://img.shields.io/pypi/v/djangocms-page-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-meta
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-page-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-meta
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-page-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-meta
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-page-meta.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-page-meta
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-page-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-page-meta?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-page-meta/develop.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-page-meta
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-page-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-page-meta
   :alt: Code Climate

Meta tag information for django CMS 3 pages

Support Python version:

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

Supported Django versions:

* Django 1.6
* Django 1.7
* Django 1.8
* Django 1.9

Supported django CMS versions:

* django CMS 3.x


**********
Quickstart
**********

#. Install djangocms-page-meta::

        $ pip install djangocms-page-meta

   or from the repository::

        pip install -e git+https://github.com/nephila/djangocms-page-meta#egg=djangocms-page-meta

#. Then add it to INSTALLED_APPS along with its dependencies::

        'filer',
        'meta',
        'meta_mixin',
        'djangocms_page_meta',

#. Synchronize the database with syncdb::

        $ python manage.py syncdb

   or migrate::

        $ python manage.py migrate

#. Configuration:

   There is no special configuration for djangocms-page-meta, but make sure you set the necessary configuration for `django-meta`_.

#. That's all!

Dependencies
============

* `django-filer`_ >= 0.9.5
* `django-meta`_  >= 0.1.0
* `django-meta-mixin`_  >= 0.1.0

.. _django-filer: https://pypi.python.org/pypi/django-filer
.. _django-meta: https://pypi.python.org/pypi/django-meta
.. _django-meta-mixin: https://pypi.python.org/pypi/django-meta-mixin

*************
Documentation
*************

For package documentation see http://djangocms-page-meta.readthedocs.org/.





*******
History
*******

0.5.10 (2016-03-03)
===================

* Fix handling Google+ author URL

0.5.9 (2016-02-25)
==================

* Fix issue with Django 1.9

0.5.8 (2016-02-23)
==================

* Improve Aldryn support
* Catch AttributeError in get_page_meta

0.5.7 (2016-01-09)
==================

* Fix handling of pages in non existing languages
* Add support for Aldryn environment

0.5.6 (2015-10-03)
==================

* Fix error when retrieing tags from djangocms-page-tags
* Add support for django CMS 3.2
* Add support for Django 1.8

0.5.5 (2015-08-21)
==================

* Different approach at fix error when page is None
* Better fallback mechanism
* Update i18n

0.5.4 (2015-08-08)
==================

* Fix error when page is None
* Code cleanup
* Add pep8/isort to tests
* Add missing migration

0.5.3 (2015-06-29)
==================

* Fix Django 1.7 migration
* Update testing configuration

0.5.2 (2015-06-28)
==================

* Compatibility with django CMS 3.1.1

0.5.1 (2015-06-06)
==================

* Make south migrations indipendent from djangocms-helper

0.5 (2015-06-06)
================

* Add support for custom user model
* Fix the length of SEO fields
* Use djangocms-helper for tests
* Add support for Django 1.7
* Add support for django CMS 3.1

0.4.1 (2014-08-10)
==================

* Minor fixes

0.4.0 (2014-04-19)
==================

* django CMS 3 final release support
* Moved some code to external django-meta-mixin application

0.3.3 (2014-03-23)
==================

* Better support for sn-dependent descriptions

0.3.2 (2014-03-07)
==================

* Add different descriptions for each supported social network

0.3.1 (2014-02-13)
==================

* Fix permission name

0.3.0 (2014-02-02)
==================

* Fix for django CMS 3 develop update

0.2.1 (2014-01-26)
==================

* Vendorizing django-meta compatibility templatetags

0.2.0 (2014-01-22)
==================

* Put toolbar menu items in a submenu

0.1.0 (2014-01-21)
==================

* Experimental release.


