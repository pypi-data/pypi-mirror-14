#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
import cherrypy
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from googleapiclient import discovery
from cocktail.styled import styled
from cocktail.controllers import Controller, Location, session
from woost import app
from woost.models import get_current_website
from woost.controllers import CMSController
from .identityprovider import GoogleIdentityProvider

SESSION_PREFIX = "woost.extensions.identity.google."


class GoogleOAuthController(Controller):

    def resolve(self, path):

        if not path:
            raise cherrypy.HTTPError(400)

        provider_id = path[0]

        try:
            provider_id = int(provider_id)
        except ValueError:
            raise cherrypy.HTTPError(400)

        provider = GoogleIdentityProvider.get_instance(provider_id)
        if provider is None:
            raise cherrypy.NotFound()

        path.pop(0)
        return GoogleOAuthProviderController(provider)


class GoogleOAuthProviderController(Controller):

    def __init__(self, provider):
        Controller.__init__(self)
        self.provider = provider
        self.target_url = (
            session.get(SESSION_PREFIX + "target_url")
            or get_current_website().home.get_uri()
        )

    def step_url(self, step_number):
        location = Location.get_current_host()
        location.path_info = "/google_oauth/%d/step%d" % (
            self.provider.id,
            step_number
        )
        return unicode(location).decode("utf-8")

    @cherrypy.expose
    def step1(self, code = None, target_url = None, **kwargs):

        if target_url:
            self.target_url = target_url
            session[SESSION_PREFIX + "target_url"] = target_url

        flow = OAuth2WebServerFlow(
            self.provider.client_id,
            self.provider.client_secret,
            self.provider.scope,
            redirect_uri = self.step_url(1)
        )
        flow.params["access_type"] = self.provider.access_type

        if not code:
            raise cherrypy.HTTPRedirect(flow.step1_get_authorize_url())

        if self.provider.debug_mode:
            print styled("Google authorization code:", "magenta"), code

        credentials = flow.step2_exchange(code)
        session[SESSION_PREFIX + "credentials"] = credentials

        if self.provider.debug_mode:
            print styled("Google refresh token:", "magenta"),
            print credentials.refresh_token
            print styled("Google access token:", "magenta"),
            print credentials.access_token

        raise cherrypy.HTTPRedirect(self.step_url(2))

    @cherrypy.expose
    def step2(self):

        credentials = session.get(SESSION_PREFIX + "credentials")

        if not credentials or credentials.access_token_expired:
            raise cherrypy.HTTPRedirect(self.step_url(1))

        http_auth = credentials.authorize(httplib2.Http())
        oauth2_service = discovery.build('oauth2', 'v2', http_auth)
        user_data = oauth2_service.userinfo().get().execute()

        if self.provider.debug_mode:
            print styled("Google user profile:", "magenta"), user_data

        self.provider.login(user_data)
        del session[SESSION_PREFIX + "credentials"]

        raise cherrypy.HTTPRedirect(self.target_url)


CMSController.google_oauth = GoogleOAuthController

