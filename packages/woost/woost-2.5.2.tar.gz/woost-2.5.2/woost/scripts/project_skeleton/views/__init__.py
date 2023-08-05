#-*- coding: utf-8 -*-
u"""
Site specific views.
"""
from pkg_resources import resource_filename
from cocktail.html import renderers, resource_repositories
renderers.default_renderer = renderers.html5_renderer

resource_repositories.define(
    "--SETUP-PACKAGE--",
    "/--SETUP-FLAT_WEBSITE_NAME--_resources",
    resource_filename("--SETUP-PACKAGE--.views", "resources")
)

