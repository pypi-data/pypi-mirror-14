memcached client for asyncio
============================

asyncio (PEP 3156) library to work with memcached.

.. image:: https://travis-ci.org/aio-libs/aiomcache.svg?branch=master
   :target: https://travis-ci.org/aio-libs/aiomcache


Getting started
---------------

The API looks very similar to the other memcache clients:

.. code:: python

    import asyncio
    import aiomcache

    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def hello_aiomcache():
        mc = aiomcache.Client("127.0.0.1", 11211, loop=loop)
        yield from mc.set(b"some_key", b"Some value")
        value = yield from mc.get(b"some_key")
        print(value)
        values = yield from mc.multi_get(b"some_key", b"other_key")
        print(values)
        yield from mc.delete(b"another_key")

    loop.run_until_complete(hello_aiomcache())


Requirements
------------

- Python >= 3.3
- asyncio https://pypi.python.org/pypi/asyncio/

CHANGES
=======

0.3.0 (03-11-2016)
----------------

- Dockerize tests

- Reuse memcached connections in Client Pool #4

- Fix stats parse to compatible more mc class software #5

0.2 (12-15-2015)
----------------

- Make the library Python 3.5 compatible

0.1 (06-18-2014)
----------------

- Initial release

