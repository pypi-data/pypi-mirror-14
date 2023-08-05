=============
WSGI Harakiri
=============

.. image:: https://img.shields.io/pypi/v/wsgi-harakiri.svg
        :target: https://pypi.python.org/pypi/wsgi-harakiri

.. image:: https://img.shields.io/travis/adamchainz/wsgi-harakiri.svg
        :target: https://travis-ci.org/adamchainz/wsgi-harakiri

WSGI Middleware that implements a customizable 'harakiri' like uWSGI.


Installation
------------

Use **pip**:

.. code-block:: bash

    pip install wsgi-harakiri

Tested on Python 2.7, 3.4, and 3.5.

Usage
-----

Wrap your WSGI application with the middleware, for example for a Django
application in your ``wsgi.py``:

.. code-block:: python

    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

    application = get_wsgi_application()

    from wsgi_harakiri import HarakiriMiddleware

    # By default adds a request timeout of 30 seconds
    application = HarakiriMiddleware(application)

Your app **must not** be running a multi-threaded server (multi-process is ok),
and it **must** be running on a POSIX system. The ``alarm`` system call is
used, so this **cannot** be combined with other things that use it, e.g. the
'harakiri' functionality in uWSGI.

API
---

``HarakiriMiddleware(application, timeout=30, on_harakiri=None, error_app=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wraps a WSGI application with the harakiri functionality.

``application`` may be any WSGI application.

``timeout`` may be any integer number of seconds, and defaults to 30.

``on_harakiri`` will be called when a harakiri occurs, from inside the alarm
function - it is thus suitable for logging the stack trace that lead to the
timeout. Its return value is ignored.

``error_app`` is a second WSGI application that will be called to produce an
error response when a timeout occurs. The default response is a rather plain
'500 Internal server error' with HTML '<h1>Page load timeout</h1>'.

Example usage with all arguments:

.. code-block:: python

    application = get_wsgi_application()

    from wsgi_harakiri import HarakiriMiddleware


    def harakiri_handler():
        logger.error("Harakiri occured", extra={'stack': True})


    def harakiri_page(environ, start_response):
        start_response(
            '500 Internal server error',
            [('Content-Type', 'text/html')]
        )
        return [b'<h1>Sorry, this page timed out.</h1>']


    application = HarakiriMiddleware(
        application,
        timeout=15,
        on_harakiri=harakiri_handler,
        error_app=harakiri_page,
    )

``Harakiri``
~~~~~~~~~~~~

This is the exception that gets raised when a timeout occurs. You should
**not** catch it anywhere in your code, however you could use it to detect when
it happens inside a particular code path. For example:

.. code-block:: python

    from wsgi_harakiri import Harakiri


    def find_users(search_term):
        conn = make_db_connection()
        try:
            return conn.query(search_term)
        except Harakiri:
            logger.error("A search timed out", extra={'search_term': search_term})
            raise
