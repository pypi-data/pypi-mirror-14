utvsapitoken
============

A little Python class that allows to check a token against `ČVUT OAAS <https://rozvoj.fit.cvut.cz/Main/oauth2>`_ and get s personal number form `Usermap API <https://rozvoj.fit.cvut.cz/Main/usermap-api>`_. Used in ÚTVS API.

Usage
-----

.. code-block:: python

   from utvsapitoken import TokenClient
   client = TokenClient()
   info = client.token_to_info('token')

You can provide custom URIs for the constructor:

.. code-block:: python

   client = TokenClient(check_token_uri='http://localhost:8080/token',
                        usermap_uri='http://localhost:8080/user'))

This comes with a fake OAAS that can be used for various testing, including the tests of this very project.
To start the fake server, just run:

.. code-block:: python

   from utvsapitoken import fakeserver
   fakeserver.serve_forever(port=8080)

In order to run the testsuite, no need to start the server, just run::

   PYTHONPATH=. py.test-3 -v --port 8080

You can omit the port argument to use the default (8080).

This requires Python 3 and ``requests``.

License
-------

This software is licensed under the terms of the MIT license, see LICENSE for full text and copyright information.
