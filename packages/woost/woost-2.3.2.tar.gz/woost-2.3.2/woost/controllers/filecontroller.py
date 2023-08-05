#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
from cocktail.controllers import serve_file
from woost.controllers.publishablecontroller import PublishableController


class FileController(PublishableController):
    """A controller that serves the files managed by the CMS."""

    def _produce_content(self, disposition = "inline", **kwargs):
        file = self.context["publishable"]
        return serve_file(
            file.file_path,
            name = file.file_name,
            content_type = file.mime_type,
            disposition = disposition
        )

