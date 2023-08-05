# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import signal

import six

__version__ = '1.0.0'


class HarakiriMiddleware(object):

    def __init__(self, app, timeout=30, on_harakiri=None, error_app=None):
        self.app = app

        if not isinstance(timeout, six.integer_types):
            raise ValueError("'timeout' must be an integer.")
        if on_harakiri is not None:
            if not callable(on_harakiri):
                raise ValueError("'on_harakiri' must be a callable.")
        self.context = HarakiriContext(timeout, on_harakiri)

        if error_app is not None:
            if not callable(error_app):
                raise ValueError("'error_app' must be a callable.")
            self.error_app = error_app
        else:
            self.error_app = simple_timeout_app

    def __call__(self, environ, start_response):
        try:
            with self.context:
                return self.app(environ, start_response)
        except Harakiri:
            return self.error_app(environ, start_response)


def simple_timeout_app(environ, start_response):
    start_response(
        '500 Internal server error',
        [('Content-Type', 'text/html')]
    )
    return [b'<h1>Page load timeout</h1>']


class HarakiriContext(object):
    def __init__(self, timeout, on_harakiri):
        self.timeout = timeout
        self.on_harakiri = on_harakiri

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_harakiri)
        signal.alarm(self.timeout)

    def __exit__(self, _, __, ___):
        signal.alarm(0)

    def raise_harakiri(self, signum, frame):
        if self.on_harakiri is not None:
            self.on_harakiri()
        raise Harakiri()


class Harakiri(Exception):
    pass
