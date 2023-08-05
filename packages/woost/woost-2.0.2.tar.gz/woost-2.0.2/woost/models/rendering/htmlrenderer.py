#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from PIL import Image
from tempfile import mkdtemp
from shutil import rmtree
from subprocess import Popen
from cocktail import schema
from woost.models.publishable import Publishable
from woost.models.user import User
from woost.models.rendering.renderer import Renderer


class HTMLRenderer(Renderer):
    """A content renderer that handles XHTML/HTML pages."""

    instantiable = True

    mime_types = set([
        "text/html",
        "text/xhtml",
        "application/xhtml"
    ])

    command = schema.String(
        required = True,
        default = "python -m woost.models.rendering.renderurl "
                  "%(source)s %(dest)s"
    )

    window_width = schema.Integer(
        min = 0
    )

    window_height = schema.Integer(
        min = 0
    )

    def can_render(self, item, **parameters):
        return (
            isinstance(item, Publishable)
            and item.mime_type in self.mime_types
            and item.is_accessible(
                user = User.get_instance(qname = "woost.anonymous_user")
            )
        )

    def render(self, item,
        window_width = None,
        window_height = None,
        **parameters
    ):
        temp_path = mkdtemp()

        try:
            temp_image_file = os.path.join(temp_path, "thumbnail.png")

            command = self.command % {
                "source": item.get_uri(host = "."),
                "dest": temp_image_file
            }

            if window_width is None:
                window_width = self.window_width

            if window_width is not None:
                command += " --min-width %d" % window_width

            if window_height is None:
                window_height = self.window_height

            if window_height is not None:
                command += " --min-width %d" % window_height

            Popen(command, shell = True).wait()
            return Image.open(temp_image_file)

        finally:
            rmtree(temp_path)

