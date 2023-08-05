#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models.block import Block


class IFrameBlock(Block):

    instantiable = True
    type_group = "blocks.custom"
    view_class = "cocktail.html.Element"

    members_order = [
        "src",
        "width",
        "height"
    ]

    src = schema.URL(
        required = True,
        member_group = "content"
    )

    width = schema.Integer(
        min = 0,
        member_group = "content"
    )

    height = schema.Integer(
        min = 0,
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.tag = "iframe"
        view["src"] = self.src
        view["frameborder"] = "0"

        if self.width:
            view["width"] = self.width

        if self.height:
            view["height"] = self.height

