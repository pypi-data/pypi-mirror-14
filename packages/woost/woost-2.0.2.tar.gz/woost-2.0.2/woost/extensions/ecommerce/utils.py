#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import cherrypy
from woost.models import get_current_website


def catalog_current_state_uri():
    catalog_url = cherrypy.request.params.get("catalog_url")
    if catalog_url:
        return catalog_url
    else:
        website = get_current_website()
        return website.ecommerce_default_catalog.get_uri()


