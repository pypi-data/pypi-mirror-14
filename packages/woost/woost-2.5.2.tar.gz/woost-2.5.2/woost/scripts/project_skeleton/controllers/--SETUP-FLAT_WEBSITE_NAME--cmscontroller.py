#-*- coding: utf-8 -*-
u"""
Provides the CMS subclass used to customize the behavior of the site.
"""
from pkg_resources import resource_filename
from cocktail.controllers import folder_publisher
from cocktail.controllers import renderingengines
from woost.controllers.cmscontroller import CMSController

renderingengines.rendering_options.update({
    "mako.directories": [
        resource_filename("--SETUP-PACKAGE--", "views"),
        resource_filename("woost", "views")
    ],
    "mako.output_encoding": "utf-8"
})


class --SETUP-WEBSITE--CMSController(CMSController):

    _cp_config = CMSController.copy_config()
    _cp_config["rendering.engine"] = "cocktail"

    class ApplicationContainer(CMSController.ApplicationContainer):
        --SETUP-FLAT_WEBSITE_NAME--_resources = folder_publisher(
            resource_filename("--SETUP-PACKAGE--.views", "resources")
        )

