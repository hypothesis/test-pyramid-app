from unittest.mock import sentinel

from pyramid.router import Router

from pyramid_app_cookiecutter_test import app


def test_create_app():
    wsgi_app = app.create_app({})

    assert isinstance(wsgi_app, Router)


def test_index():
    assert app.index(sentinel.request) == {"Hello": "Pyramid!"}


def test_status():
    assert app.status(sentinel.request) == {"status": "okay"}
