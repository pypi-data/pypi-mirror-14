Ubersmith API Client for Python
===============================

.. image:: https://travis-ci.org/internap/python-ubersmithclient.svg?branch=master
    :target: https://travis-ci.org/internap/python-ubersmithclient

.. image:: https://img.shields.io/pypi/v/ubersmith_client.svg?style=flat
    :target: https://pypi.python.org/pypi/ubersmith_client

Usage
-----
.. code:: python

    import ubersmith_client

    api = ubersmith_client.api.init('http://ubersmith.com/api/2.0/', 'username', 'password')
    api.client.count()
     >>> u'264'
    api.client.latest_client()
     >>> 1265

API
---------

**ubersmith_client.api.init(url, user, password, timeout, use_http_post)**
 :url:
   URL of your API

   *Example:* ``http://ubersmith.example.org/api/2.0/``

 :user: API username
 :password: API Password or token
 :timeout: api timeout given to requests

   *Default:* ``60``
 :use_http_post:
   Use `POST` requests instead of `GET`

   *Default:* ``False``
