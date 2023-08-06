Ubersmith API Client for Python
===============================

.. image:: https://travis-ci.org/internap/python-ubersmithclient.svg?branch=master
    :target: https://travis-ci.org/internap/python-ubersmithclient

.. image:: https://img.shields.io/pypi/v/python-ubersmithclient.svg?style=flat
    :target: https://pypi.python.org/pypi/python-ubersmithclient

Usage
-----
.. code:: python

    import ubersmith_client

    api = ubersmith_client.api.init(url='http://ubersmith.com/api/2.0/', user='username', password='password')
    api.client.count()
     >>> u'264'
    api.client.latest_client()
     >>> 1265

API
---------

**ubersmith_client.api.init(url, user, password, timeout, use_http_get)**
 :url:
   URL of your API

   *Example:* ``http://ubersmith.example.org/api/2.0/``

 :user: API username
 :password: API Password or token
 :timeout: api timeout given to requests

   *Default:* ``60``
 :use_http_get:
   Use `GET` requests instead of `POST`

   *Default:* ``False``
