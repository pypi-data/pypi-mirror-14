# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import signal
import subprocess
import time
from contextlib import contextmanager

import pytest
import requests

from wsgi_harakiri import HarakiriMiddleware


@contextmanager
def run_gunicorn(app_name):
    command = ['gunicorn', __name__ + ':' + app_name]
    process = subprocess.Popen(command)
    time.sleep(1)  # Let gunicorn start
    try:
        yield
    finally:
        process.send_signal(signal.SIGINT)
        process.wait()


def test_times_out():
    with run_gunicorn('app_times_out'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 500
        assert b'Page load timeout' in resp.content


def app_times_out(environ, start_response):
    time.sleep(1.1)

app_times_out = HarakiriMiddleware(app_times_out, 1)


def test_does_not_time_out():
    with run_gunicorn('app_does_not_time_out'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 200
        assert resp.content == b'<h1>Fine</h1>'


def app_does_not_time_out(environ, start_response):
    start_response(
        '200 OK',
        [('Content-Type', 'text/html')]
    )
    return [b'<h1>Fine</h1>']

app_does_not_time_out = HarakiriMiddleware(app_does_not_time_out, 2)


def test_custom_handler():
    with run_gunicorn('app_custom_handler'):
        resp = requests.get('http://localhost:8000')
        # Error page from gunicorn itself
        assert resp.status_code == 500
        assert b'<h1><p>Internal Server Error</p></h1>' in resp.content


def app_custom_handler(environ, start_response):
    time.sleep(1.1)


def custom_handler():
    raise ValueError()

app_custom_handler = HarakiriMiddleware(app_custom_handler, 1, custom_handler)


def test_custom_error():
    with run_gunicorn('app_custom_error'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 418
        assert resp.content == b"I'm a teapot"


def app_custom_error(environ, start_response):
    time.sleep(1.1)


def custom_error(environ, start_response):
    start_response(
        "418 I'm a teapot",
        [('Content-Type', 'text/plain')]
    )
    return [b"I'm a teapot"]


app_custom_error = HarakiriMiddleware(app_custom_error, 1, error_app=custom_error)


def test_timeout_must_be_integer():
    with pytest.raises(ValueError) as excinfo:
        HarakiriMiddleware(None, 1.5)
    assert "'timeout' must be an integer." in str(excinfo.value)


def test_on_harakiri_must_be_callable():
    with pytest.raises(ValueError) as excinfo:
        HarakiriMiddleware(None, on_harakiri=13)
    assert "'on_harakiri' must be a callable." in str(excinfo.value)


def test_error_app_must_be_callable():
    with pytest.raises(ValueError) as excinfo:
        HarakiriMiddleware(None, error_app=13)
    assert "'error_app' must be a callable." in str(excinfo.value)
