`XCACHE <https://pypi.python.org/pypi/clean_cache>`_
====================================================

It's like `lru_caches <https://docs.python.org/3/library/functools.html#functools.lru_cache>`_ but can be cleared automatically or via context managers.


Why?
----

`There are only two hard things in Computer Science: cache invalidation and naming things. <http://martinfowler.com/bliki/TwoHardThings.html>`_

-- Phil Karlton

So, caches are fairly easy, but their invalidation is kind of hard to get right.


What type of cache is used?
---------------------------

The default implementation is the lru_cache of the stdlib but you can drop in your own.


How?
----

Python features garbage collection aka. automatic memory management. Let's make use of it:

.. code:: python

    from clean_cache import ref_cache

    request_cache = ref_cache_gen(lambda: request)  # default cache_impl=lru_cache


Here, we defined our own cache that needs the global request for invalidating the cache.
As soon as ``request`` is garbage-collected, the cached data is freed.

.. code:: python

    @request_cache()
    def fib(n):
        return fib(n-1) + fib(n-2) if n > 1 else 1


Here, we see how to decorate a function to work like a lru_cache.

Now, let's see how this works:

.. code:: python

    class Request(): pass

    request = Request()

    print(fib(10))
    print(fib(20))
    print(fib.cache_info())  # fib cache contains 2 items

    request = Request()      # invalidates all caches

    print(fib.cache_info())  # fib cache contains 0 items
    print(fib(10))
    print(fib(20))


Context Manager for more more control over cache invalidation
-------------------------------------------------------------

If you need more control, the context manager ``clean_caches`` is what you need:

.. code:: python

    from clean_cache import ref_cache, clean_caches

    @ref_cache()
    def fib(n):
        return fib(n-1) + fib(n-2) if n > 1 else 1

    with clean_caches():
        print(fib(10))
        print(fib(20))
        print(fib.cache_info())  # fib cache contains 2 items
    print(fib.cache_info())      # fib cache contains 0 items


You can even specify what object the caches should be attached to:

.. code:: python

    from clean_cache import ref_cache, clean_caches

    @ref_cache()
    def fib(n):
        return fib(n-1) + fib(n-2) if n > 1 else 1

    with clean_caches(Request()) as request:
        print(fib(10))
        print(fib(20))
        print(fib.cache_info())  # fib cache contains 2 items
    print(fib.cache_info())      # fib cache contains 0 items


Can these context managers be nested?
-------------------------------------

Sure. At each entrance and and exit of each context, all associated caches are emptied.


Conclusion
----------

Good
****

- cache invalidation done easy
- works via garbage collection
- works via context managers
- works with Python2 and Python3

Bad
***

- unkown ;-)


Ideas are always welcome. :-)
