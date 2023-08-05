#-*- coding: utf-8 -*-
u"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			May 2010
"""
from warnings import warn
import cherrypy
from woost.controllers import BaseCMSController


class FirstChildRedirectionController(BaseCMSController):

    def __call__(self, *args, **kwargs):

        warn(
            "FirstChildRedirectionController is deprecated, "
            "use Document.redirection_mode instead",
            DeprecationWarning
        )

        publishable = self.context["publishable"]

        if hasattr(publishable,"children"):

            for child in publishable.children:
                if child.is_accessible():
                    raise cherrypy.HTTPRedirect(uri.get_uri())

        raise cherrypy.HTTPError(404)

