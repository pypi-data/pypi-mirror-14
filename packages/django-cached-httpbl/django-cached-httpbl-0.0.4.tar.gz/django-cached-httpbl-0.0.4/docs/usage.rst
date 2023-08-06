Configuration
=============


Cached httpBL settings
----------------------

You have several options available to you in ``django-cached-httpbl`.
These options should be defined in your ``settings.py`` file.

* ``CACHED_HTTPBL_API_KEY``:

    Your httpBL API key, you should register on http://projecthoneypot.org to get one.

* ``CACHED_HTTPBL_API_HOST``: httpBL API host (default: 'dnsbl.httpbl.org')

* ``CACHED_HTTPBL_API_TIMEOUT``: timeout (seconds) for httpBL requests (default: 5)

* ``CACHED_HTTPBL_HARMLESS_AGE``:

    Age (days), after this age IP _probably_ is harmless, but still in blacklist (default: 14)

* ``CACHED_HTTPBL_ALLOWED_THREAT_SCORE``: allowed threat score (default: 5)

* ``CACHED_HTTPBL_USE_CACHE``: use Django cache for httpBL (default: True)

* ``CACHED_HTTPBL_CACHE_BACKEND``: Django cache backend, if not provided, default Django db is used for cache

* ``CACHED_HTTPBL_CACHE_TIMEOUT``: cache invalidation timeout (seconds) (default: 86400)

* ``CACHED_HTTPBL_REDIRECT_URL``: redirect url for bad traffic redirection (default: None)

* ``CACHED_HTTPBL_RESPONSE_NOT_FOUND_HTML``: html for middleware http response not found (default: '<h1>Not Found</h1>')

* ``CACHED_HTTPBL_IGNORE_REQUEST_METHODS``: ignore bad traffic for these request methods (default: ())

* ``CACHED_HTTPBL_USE_LOGGING``:

    Use bad IP's logging if you use middleware (default: False)
    You should setup ``cached_httpbl`` logger handler in your Django settings, before enable this option


Usage
=====

Use package sources and ``example_app`` in the ``docs`` directory as guide.

Cached httpBL API
-----------------

You can use cached httpBL API if you need doing something with httpBL check results,
but do not want use middleware from this package.

.. code:: python

    httpBL = CachedHTTPBL()
    result = httpBL.check_ip('127.0.0.1')
    is_suspicious = httpBL.is_suspicious(result)
    is_threat = httpBL.is_threat(result)


Cached httpBL view middleware
-----------------------------

You can add cached httpBL view middleware to your Django settings:

.. code:: python
    MIDDLEWARE_CLASSES = (
    ...
        'cached_httpbl.middleware.CachedHTTPBLViewMiddleware',
    ...
    )

When you use this middleware you can hide your site from bad IP traffic or setup allowed http methods for bad IP's.


Cached httpBL decorators
------------------------

You can add cached httpBL protection or disable it on per view basis.
For enable cached httpBL protection to view use ``@cached_httpbl_protect`` decorator.

.. code:: python

    from cached_httpbl.decorators import cached_httpbl_protect

    @cached_httpbl_protect
    def protected_view():
        pass

For disable cached httpBL protection for view use ``@cached_httpbl_exempt`` decorator.

.. code:: python

    from cached_httpbl.decorators import ached_httpbl_exempt

    @cached_httpbl_exempt
    def protected_view():
        pass
