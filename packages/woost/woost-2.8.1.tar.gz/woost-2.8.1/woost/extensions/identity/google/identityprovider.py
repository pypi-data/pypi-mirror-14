#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
import json
import urllib
import urllib2
from cocktail.styled import styled
from cocktail import schema
from cocktail.controllers import Location
from woost import app
from woost.models import Configuration
from woost.extensions.identity.identityprovider import IdentityProvider


class GoogleIdentityProvider(IdentityProvider):

    provider_name = "Google"
    user_identifier = "google_user_id"

    members_order = [
        "client_id",
        "client_secret",
        "scope",
        "access_type"
    ]

    client_id = schema.String(
        required = True,
        text_search = False
    )

    client_secret = schema.String(
        required = True,
        text_search = False
    )

    scope = schema.Collection(
        min = 1,
        default = schema.DynamicDefault(lambda: ["profile", "email"]),
        items = schema.String()
    )

    access_type = schema.String(
        required = True,
        default = "online",
        enumeration = ["online", "offline"],
        edit_control = "cocktail.html.RadioSelector"
    )

    def get_auth_url(self, target_url = None):
        return (
            "/google_oauth/%d/step1?%s" % (
                self.id,
                urllib.urlencode({
                    "target_url": target_url
                                  or unicode(
                        Location.get_current(relative=False)).encode("utf-8")
                })
            )
        )

    def get_refresh_token_url(self, redirect_uri = None):
        """
        Produces the URL to initiate a browser driven request to get a refresh
        code.
        """
        OAUTH_URL = "https://accounts.google.com/o/oauth2/auth"

        if not redirect_uri:
            website = (app.website or Configuration.instance.websites[0])
            redirect_uri = "http://%s/google_oauth/%d/refresh_token" % (
                website.hosts[0],
                self.id
            )

        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.scope),
            "response_type": "code",
            "access_type": self.access_type,
            "approval_prompt": "force"
        }

        return "{}?{}".format(OAUTH_URL, urllib.urlencode(params))

    def get_refresh_token_from_browser(self, redirect_uri = None):
        """
        Opens the browser to get user authorization and shows the
        authorization code.
        """
        import webbrowser
        url = self.get_refresh_token_url(redirect_uri)
        webbrowser.open(url)

    def get_refresh_token(self, code, redirect_uri = None):
        """
        Gets an authorization token with access_token and refresh_token from
        an authorization code.

        :param code: A valid authorization code with access_type offline
        :return: A dict representing the authorization token. The
        'access_token' key is a valid access token and the 'refresh_token'
        key can be used to generate new valid access tokens
        """
        TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

        if not redirect_uri:
            website = (app.website or Configuration.instance.websites[0])
            redirect_uri = "http://%s/google_oauth/%d/refresh_token" % (
                website.hosts[0],
                self.id
            )

        params = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }

        request = urllib2.Request(url=TOKEN_URL, data=urllib.urlencode(params))
        json_file = urllib2.urlopen(request).read()
        auth_token = json.loads(json_file)

        if self.debug_mode:
            print styled("Google refresh token:", "magenta"), auth_token

        return auth_token

    def get_access_token_from_refresh_token(self, refresh_token):
        """
        Gets a new access token from a refresh token.

        :return: A dict respresenting an access token. Its 'access_token' key
        is a valid access token
        """
        TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }

        request = urllib2.Request(url=TOKEN_URL, data=urllib.urlencode(params))

        try:
            json_file = urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            if self.debug_mode:
                print styled(
                    "Error while obtaining a Google access token from a "
                    "refresh token:",
                    "magenta"
                )
                print e.read()
            raise

        access_token = json.loads(json_file)

        if self.debug_mode:
            print styled("Google access token from refresh token:", "magenta"),
            print access_token

        return access_token

