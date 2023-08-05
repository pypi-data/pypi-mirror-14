#-*- coding: utf-8 -*-
u"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			March 2009
"""
import cherrypy
from cocktail.controllers import get_state
from woost.controllers import BaseCMSController


class URIController(BaseCMSController):

    def __call__(self, *args, **kwargs):

        if self.is_internal_content():
            parameters = get_state()
        else:
            parameters = None

        uri = self.context["publishable"].get_uri(parameters = parameters)
        raise cherrypy.HTTPRedirect(uri)

