#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Slot, Block, ElementType


class OrderStepsContainerBlock(Block):

    instantiable = True
    type_group = "blocks.ecommerce"
    view_class = "woost.extensions.ecommerce.OrderStepsContainerBlockView"

    members_order = [
        "list_type"
    ]

    list_type = schema.String(
        required = True,
        default = "div",
        enumeration = [
            "div",
            "ul",
            "ol",
            "dl"
        ],
        member_group = "content"
    )

    blocks = Slot()

    def init_view(self, view):
        Block.init_view(self, view)
        view.step_content.tag = self.list_type
        view.blocks = self.blocks
        return view

