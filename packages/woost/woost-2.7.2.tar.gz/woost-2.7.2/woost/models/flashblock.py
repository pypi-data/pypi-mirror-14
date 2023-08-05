#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .file import File
from .block import Block


class FlashBlock(Block):

    instantiable = True
    view_class = "cocktail.html.SWFObject"

    members_order = [
        "swf_file",
        "width",
        "height",
        "flash_version",
        "flash_vars",
        "flash_params",
        "flash_attributes"
    ]

    swf_file = schema.Reference(
        type = File,
        rquired = True,
        relation_constraints = {"mime_type": "application/x-shockwave-flash"},
        related_end = schema.Collection(),
        member_group = "content"
    )

    width = schema.Integer(
        required = True,
        min = 0,
        member_group = "content"
    )

    height = schema.Integer(
        required = True,
        min = 0,
        member_group = "content"
    )

    flash_version = schema.String(
        required = True,
        default = "9.0.0",
        member_group = "content"
    )

    flash_vars = schema.String(
        edit_control = "cocktail.html.TextArea",
        member_group = "content"
    )

    flash_params = schema.String(
        edit_control = "cocktail.html.TextArea",
        member_group = "content"
    )

    flash_attributes = schema.String(
        edit_control = "cocktail.html.TextArea",
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.flash_file = self.swf_file.get_uri()
        view.flash_width = self.width
        view.flash_height = self.height
        view.flash_version = self.flash_version
        view.flash_vars = self._split_config(self.flash_vars)
        view.flash_params = self._split_config(self.flash_params)
        view.flash_attributes = self._split_config(self.flash_attributes)

    def _split_config(self, config_text):

        config = {}

        if config_text:
            for line in config_text.split("\n"):
                try:
                    pos = line.find("=")
                    key = line[:pos]
                    value = line[pos + 1:]
                except:
                    pass
                else:
                    config[key.strip()] = value.strip()

        return config

