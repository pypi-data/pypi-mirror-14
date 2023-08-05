#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block
from .document import Document


class MenuBlock(Block):

    instantiable = True
    view_class = "woost.views.Menu"

    root = schema.Reference(
        type = Document,
        related_end = schema.Collection(),
        member_group = "content"
    )

    root_visible = schema.Boolean(
        required = True,
        default = False,
        member_group = "content"
    )

    max_depth = schema.Integer(
        member_group = "content"
    )

    expanded = schema.Boolean(
        required = True,
        default = False,
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.root = self.root
        view.root_visible = self.root_visible
        view.max_depth = self.max_depth
        view.expanded = self.expanded

