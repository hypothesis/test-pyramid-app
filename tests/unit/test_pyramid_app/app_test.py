from unittest.mock import sentinel

import pytest
from pyramid.router import Router
from pyramid.testing import DummyRequest

from test_pyramid_app import app


def test_create_app():
    wsgi_app = app.create_app({})

    assert isinstance(wsgi_app, Router)


def test_index():
    assert app.index(sentinel.request) == {"Hello": "Pyramid!"}


def test_status(capture_message):
    request = DummyRequest(path="/_status")

    assert app.status(request) == {"status": "okay"}

    capture_message.assert_not_called()


def test_status_sends_test_messages_to_sentry(capture_message):
    request = DummyRequest(params={"sentry": ""}, path="/_status")

    app.status(request)

    capture_message.assert_called_once_with(
        "Test message from test-pyramid-app's status view"
    )


@pytest.fixture(autouse=True)
def capture_message(mocker):
    return mocker.patch(
        "test_pyramid_app.app.capture_message", autospec=True, spec_set=True
    )
