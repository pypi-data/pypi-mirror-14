#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import cherrypy
from raven import Client
from cocktail.events import when
from pkg_resources import get_distribution
from woost import app
from woost.models import AuthorizationError
from woost.authenticationscheme import AuthenticationFailedError
from woost.controllers import CMSController


def register(dsn):
    app.sentry = Sentry(Client(dsn))

    @when(CMSController.exception_raised)
    def handle_exception(event):
        error = event.exception
        app.sentry.capture_exception(exception = error)


class Sentry(object):

    def __init__(self, client):
        self.client = client
        self.tags = {
            "framework": "woost",
            "woost": get_distribution("woost").version,
            "cocktail": get_distribution("cocktail").version
        }

    def get_data_from_request(self):
        """Returns request data extracted from cherrypy.request."""
        request = cherrypy.request
        return {
            'sentry.interfaces.Http': {
                'url': cherrypy.url(),
                'query_string': request.query_string,
                'method': request.method,
                'data': request.params,
                'headers': request.headers,
                'env': {
                    'SERVER_NAME': cherrypy.server.socket_host,
                    'SERVER_PORT': cherrypy.server.socket_port
                }
            }
        }

    def update_context(self, kwargs):
        data = kwargs.get('data')
        if data is None:
            kwargs['data'] = self.get_data_from_request()

        tags = self.tags.copy()
        if "tags" in kwargs:
            tags.update(kwargs["tags"])

        kwargs["tags"] = tags

    def should_capture_exception(self, exception):
        is_http_error = isinstance(exception, cherrypy.HTTPError)

        return (
            (is_http_error and exception.status == 500)
            or (
                not is_http_error
                and not isinstance(
                    exception, (AuthorizationError, AuthenticationFailedError)
                )
            )
        )

    def capture_exception(self, exception, **kwargs):
        if self.should_capture_exception(exception):
            self.update_context(kwargs)
            return self.client.captureException(**kwargs)

    def capture_message(self, message, **kwargs):
        self.update_context(**kwargs)
        return self.client.captureMessage(message, **kwargs)

