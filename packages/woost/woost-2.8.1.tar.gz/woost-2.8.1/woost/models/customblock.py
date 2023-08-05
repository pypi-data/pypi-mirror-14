#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block


class CustomBlock(Block):

    instantiable = True
    type_group = "blocks.custom"

    view_class = schema.String(
        required = True,
        shadows_attribute = True,
        before_member = "controller",
        member_group = "behavior"
    )

