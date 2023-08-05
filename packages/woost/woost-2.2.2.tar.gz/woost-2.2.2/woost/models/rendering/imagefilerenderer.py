#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from cocktail import schema
from cocktail.controllers.imageupload import get_image_size
from woost.models.file import File
from woost.models.rendering.renderer import Renderer
from woost.models.rendering.formats import formats_by_mime_type


class ImageFileRenderer(Renderer):
    """A content renderer that handles image files."""

    instantiable = True

    max_size = schema.Tuple(
        items = (
            schema.Integer(
                required = True,
                min = 1
            ),
            schema.Integer(
                required = True,
                min = 1
            )
        ),
        request_value_separator = "x"
    )

    def can_render(self, item, **parameters):
        return (
            isinstance(item, File)
            and item.resource_type == "image"
            and item.mime_type in formats_by_mime_type
            and (self.max_size is None or self.validate_size(item))
        )

    def validate_size(self, file):
        try:
            width, height = get_image_size(file.file_path)
        except IOError:
            return False
        else:
            max_size = self.max_size
            return (width <= max_size[0] and height <= max_size[1]) \
                or (width <= max_size[1] and height <= max_size[0])

    def render(self, item, **parameters):
        return item.file_path

