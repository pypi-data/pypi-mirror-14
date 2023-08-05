#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block
from .publishable import Publishable


class FacebookLikeButton(Block):

    instantiable = True
    type_group = "blocks.social"
    view_class = "cocktail.html.FacebookLikeButton"

    members_order = [
        "fb_href",
        "fb_layout",
        "fb_send",
        "fb_show_faces",
        "fb_width",
        "fb_action",
        "fb_font",
        "fb_colorscheme",
        "fb_ref"
    ]

    fb_href = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "content"
    )

    fb_layout = schema.String(
        required = True,
        default = "standard",
        enumeration = ["standard", "button_count", "box_count"],
        member_group = "appearence"
    )

    fb_send = schema.Boolean(
        default = False,
        required = True,
        member_group = "appearence"
    )

    fb_show_faces = schema.Boolean(
        default = False,
        required = True,
        member_group = "appearence"
    )

    fb_width = schema.Integer(
        required = True,
        default = 450,
        member_group = "appearence"
    )

    fb_action = schema.String(
        required = True,
        default = "like",
        enumeration = ["like", "recommend"],
        member_group = "appearence"
    )

    fb_font = schema.String(
        required = True,
        default = "arial",
        enumeration = [
            "arial",
            "lucida grande",
            "segoe ui",
            "tahoma",
            "trebuchet ms",
            "verdana"
        ],
        translatable_enumeration = False,
        member_group = "appearence"
    )

    fb_colorscheme = schema.String(
        required = True,
        default = "light",
        enumeration = ["light", "dark"],
        member_group = "appearence"
    )

    fb_ref = schema.String(
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.href = self.fb_href and self.fb_href.get_uri(host = ".")
        view.send = self.fb_send
        view.layout = self.fb_layout
        view.show_faces = self.fb_show_faces
        view.width = self.fb_width
        view.action = self.fb_action
        view.font = self.fb_font
        view.colorscheme = self.fb_colorscheme
        view.ref = self.fb_ref

