#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import Configuration
from woost.extensions.blocks.block import Block
from woost.extensions.blocks.elementtype import ElementType
from woost.extensions.issuu.issuudocument import IssuuDocument


class IssuuBlock(Block):

    instantiable = True
    view_class = "woost.extensions.issuu.IssuuBlockView"
    block_display = "woost.extensions.issuu.IssuuBlockDisplay"

    members_order = ["element_type", "issuu_document", "width", "height"]

    element_type = ElementType(
        member_group = "content"
    )

    issuu_document = schema.Reference(
        type = IssuuDocument,
        required = True,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "content"
    )

    width = schema.Integer(
        listed_by_default = False,
        member_group = "content"
    )

    height = schema.Integer(
        listed_by_default = False,
        member_group = "content"
    )

