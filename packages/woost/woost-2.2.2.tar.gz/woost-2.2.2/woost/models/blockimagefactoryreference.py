#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.html.datadisplay import display_factory
from cocktail.iteration import first
from .configuration import Configuration
from .rendering import ImageFactory

def _iter_block_image_factories():
    for factory in Configuration.instance.image_factories:
        if factory.applicable_to_blocks:
            yield factory

def _block_image_factories_enumeration(ctx):
    return list(_iter_block_image_factories())

_block_image_factories_default = schema.DynamicDefault(
    lambda: first(_iter_block_image_factories())
)

_mandatory_dropdown = display_factory(
    "cocktail.html.DropdownSelector",
    empty_option_displayed = False
)


class BlockImageFactoryReference(schema.Reference):

    def __init__(self, *args, **kwargs):

        kwargs.setdefault("required", True)
        kwargs.setdefault("type", ImageFactory)
        kwargs.setdefault("enumeration", _block_image_factories_enumeration)
        kwargs.setdefault("default", _block_image_factories_default)
        kwargs.setdefault("edit_control", _mandatory_dropdown)

        if "bidirectional" not in kwargs and "related_end" not in kwargs:
            kwargs["related_end"] = schema.Collection()

        schema.Reference.__init__(self, *args, **kwargs)

