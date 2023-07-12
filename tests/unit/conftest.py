import pytest
from pyramid import testing
from pyramid.request import apply_request_extensions


@pytest.fixture
def pyramid_config(pyramid_settings):
    with testing.testConfig(settings=pyramid_settings) as pyramid_config:
        yield pyramid_config


@pytest.fixture
def pyramid_request(
    db_session,
    pyramid_config,  # pylint:disable=unused-argument
):
    pyramid_request = testing.DummyRequest()
    apply_request_extensions(pyramid_request)
    pyramid_request.db = db_session
    return pyramid_request
