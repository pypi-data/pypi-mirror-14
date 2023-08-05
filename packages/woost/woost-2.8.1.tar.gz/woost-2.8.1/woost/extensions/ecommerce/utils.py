#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import cherrypy
from woost import app


def catalog_current_state_uri():
    catalog_url = cherrypy.request.params.get("catalog_url")
    if catalog_url:
        return catalog_url
    else:
        website = app.website
        if website.ecommerce_default_catalog:
            return website.ecommerce_default_catalog.get_uri()


