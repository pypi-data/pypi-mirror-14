# Ubersmith API Client for Python

.. image:: https://travis-ci.org/internap/python-ubersmithclient.svg?branch=master
    :target: https://travis-ci.org/internap/python-ubersmithclient

.. image:: https://img.shields.io/pypi/v/ubersmith_client.svg?style=flat
    :target: https://pypi.python.org/pypi/ubersmith_client

# Usage

    >>> import ubersmith_client
    >>> api = ubersmith_client.api.init('http://ubersmith.com/api/2.0/', 'username', 'password')
    >>> api.client.count()
    u'264'
    >>> api.client.latest_client()
    1265
