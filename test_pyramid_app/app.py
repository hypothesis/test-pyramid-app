from dataclasses import dataclass
from os import environ

import pyramid_googleauth
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allowed, Denied
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import forbidden_view_config, view_config, view_defaults
from sentry_sdk import capture_message

from test_pyramid_app._version import get_version
from test_pyramid_app.celery import work


class GoogleSecurityPolicy(pyramid_googleauth.GoogleSecurityPolicy):  # pragma: no cover
    @dataclass
    class Identity:
        permissions: list[str]

    def identity(self, request):
        userid = self.authenticated_userid(request)

        if userid:
            return self.Identity(permissions=["admin"])

        return self.Identity([])

    def permits(self, request, _context, permission):
        if permission in self.identity(request).permissions:
            return Allowed("allowed")

        return Denied("denied")


def create_app(_=None, **settings):
    settings["pyramid_googleauth.google_client_id"] = environ[
        "PYRAMID_GOOGLEAUTH_CLIENT_ID"
    ]
    settings["pyramid_googleauth.google_client_secret"] = environ[
        "PYRAMID_GOOGLEAUTH_CLIENT_SECRET"
    ]
    settings["pyramid_googleauth.secret"] = environ["PYRAMID_GOOGLEAUTH_SECRET"]

    with Configurator(settings=settings) as config:
        config.add_route("index", "/")
        config.add_route("status", "/_status")
        config.add_route("admin", "/admin")

        config.set_session_factory(
            SignedCookieSessionFactory(environ["SESSION_COOKIE_SECRET"])
        )
        config.set_security_policy(GoogleSecurityPolicy())
        config.include("pyramid_googleauth")

        config.include("pyramid_jinja2")

        # Enable Sentry's "Releases" feature, see:
        # https://docs.sentry.io/platforms/python/configuration/options/#release
        #
        # h_pyramid_sentry passes any h_pyramid_sentry.init.* Pyramid settings
        # through to sentry_sdk.init(), see:
        # https://github.com/hypothesis/h-pyramid-sentry?tab=readme-ov-file#settings
        #
        # For the full list of options that sentry_sdk.init() supports see:
        # https://docs.sentry.io/platforms/python/configuration/options/
        settings["h_pyramid_sentry.init.release"] = get_version()

        config.include("h_pyramid_sentry")

        config.scan()

        return config.make_wsgi_app()


@view_config(route_name="index", renderer="json")
def index(_request):
    return {"Hello": "Pyramid!"}


@view_config(route_name="status", renderer="json", http_cache=0)
def status(request):
    if "sentry" in request.params:
        capture_message("Test message from test-pyramid-app's status view")

    return {"status": "okay"}


@forbidden_view_config(route_name="admin")
def logged_out(request):  # pragma: no cover
    return HTTPFound(
        location=request.route_url(
            "pyramid_googleauth.login", _query={"next": request.url}
        ),
    )


@view_defaults(route_name="admin", permission="admin")
class AdminViews:  # pragma: no cover
    def __init__(self, _context, request):
        self.request = request

    @view_config(
        request_method="GET", renderer="test_pyramid_app:templates/admin.html.jinja2"
    )
    def get(self):
        return {}

    @view_config(request_method="POST")
    def post(self):
        seconds = int(self.request.POST["work_for"])

        work.delay(seconds)

        return HTTPFound(self.request.route_url("admin"))
