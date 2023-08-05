#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .slot import Slot
from .block import Block
from .elementtype import ElementType


class ContainerBlock(Block):

    instantiable = True
    type_group = "blocks.layout"
    view_class = "woost.views.ContainerBlockView"

    members_order = [
        "element_type",
        "list_type"
    ]

    element_type = ElementType(
        member_group = "content"
    )

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

        if self.element_type == "dd":
            view.tag = None
            view.blocks_list.tag = "dd"
        else:
            view.tag = self.element_type

        view.blocks_list.tag = self.list_type
        view.blocks = self.blocks
        return view

    def get_block_proxy(self, view):
        if self.element_type == "dd":
            return view.blocks_list
        return view

