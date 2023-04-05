import pytest
from webtest import TestApp

from test_pyramid_app.app import create_app


def test_index(app):
    assert app.get("/").json == {"Hello": "Pyramid!"}


def test_status(app):
    assert app.get("/_status").json == {"status": "okay"}


@pytest.fixture
def app():
    return TestApp(create_app({}))
