#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block
from .publishable import Publishable


class FacebookLikeBox(Block):

    instantiable = True
    type_group = "blocks.social"
    view_class = "cocktail.html.FacebookLikeBox"

    members_order = [
        "fb_href",
        "fb_show_faces",
        "fb_stream",
        "fb_header",
        "fb_width",
        "fb_height",
        "fb_border_color",
        "fb_colorscheme"
    ]

    fb_href = schema.URL(
        required = True,
        member_group = "content"
    )

    fb_show_faces = schema.Boolean(
        default = True,
        required = True,
        member_group = "appearence"
    )

    fb_stream = schema.Boolean(
        default = False,
        required = True,
        member_group = "appearence"
    )

    fb_header = schema.Boolean(
        default = False,
        required = True,
        member_group = "appearence"
    )

    fb_width = schema.Integer(
        required = True,
        default = 292,
        member_group = "appearence"
    )

    fb_height = schema.Integer(
        member_group = "appearence"
    )

    fb_border_color = schema.Color(
        member_group = "appearence"
    )

    fb_colorscheme = schema.String(
        required = True,
        default = "light",
        enumeration = ["light", "dark"],
        member_group = "appearence"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.href = self.fb_href
        view.show_faces = self.fb_show_faces
        view.stream = self.fb_stream
        view.header = self.fb_header
        view.width = self.fb_width
        view.height = self.fb_height
        view.border_color = self.fb_border_color
        view.colorscheme = self.fb_colorscheme

