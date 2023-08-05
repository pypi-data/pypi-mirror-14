==================================
django-gddkia-impediments-on-roads
==================================

.. image:: https://codeclimate.com/github/tomi77/django-gddkia-impediments-on-roads/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/django-gddkia-impediments-on-roads
   :alt: Code Climate
.. image:: https://travis-ci.org/tomi77/django-gddkia-impediments-on-roads.svg?branch=master
   :target: https://travis-ci.org/tomi77/django-gddkia-impediments-on-roads
.. image:: https://coveralls.io/repos/github/tomi77/django-gddkia-impediments-on-roads/badge.svg?branch=master
   :target: https://coveralls.io/github/tomi77/django-gddkia-impediments-on-roads?branch=master

Installation
============

Install package via ``pip``
::

    pip install django-gddkia-impediments-on-roads

Configuration
=============

Configure cache options
::

   # Cache backend name
   IMPEDIMENTS_CACHE_BACKEND_NAME = 'default'

   # Cache key
   IMPEDIMENTS_CACHE_KEY = 'impediments'

   # Max time of cache
   IMPEDIMENTS_CACHE_TIMEOUT = 3600

API Usage
=========

::

    from dj_impediments import get_impediments

    print get_impediments()
