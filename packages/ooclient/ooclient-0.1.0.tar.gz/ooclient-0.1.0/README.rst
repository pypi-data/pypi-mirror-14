Simple library to connect to OOServer
=====================================

At this moment the only mission of this library is to use erppeek as a
client lib but accepting an URL to connect to OpenObject Server.

Eg.

.. code-block:: python

    from ooclient import Client
    c = Client('http://user:password@server:port/database')

