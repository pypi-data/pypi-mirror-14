#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import cherrypy
from woost.controllers import BaseCMSController


class IssuuDocumentController(BaseCMSController):

    def __call__(self, *args, **kwargs):
        uri = self.context["publishable"].get_issuu_uri()
        raise cherrypy.HTTPRedirect(uri)


