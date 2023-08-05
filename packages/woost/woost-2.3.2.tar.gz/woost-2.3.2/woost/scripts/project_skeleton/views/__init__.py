#-*- coding: utf-8 -*-
u"""
Site specific views.
"""
from pkg_resources import resource_filename
from cocktail.html import renderers, resource_repositories
renderers.default_renderer = renderers.html5_renderer

resource_repositories.define(
    "_PROJECT_MODULE_",
    "/_PROJECT_MODULE__resources",
    resource_filename("_PROJECT_MODULE_.views", "resources")
)

