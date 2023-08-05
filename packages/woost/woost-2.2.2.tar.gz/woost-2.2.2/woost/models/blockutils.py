#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block
from .slot import Slot


def type_is_block_container(cls):

    for member in cls.members().itervalues():
        if (
            isinstance(member, schema.RelationMember)
            and member.related_type
            and issubclass(member.related_type, Block)
            and member.visible and member.editable
        ):
            return True

    return any(
        type_is_block_container(subclass)
        for subclass in cls.derived_schemas(recursive = False)
    )

def find_blocks(obj, slots = None):

    if isinstance(obj, Block):
        yield obj

    if slots is None:
        slots = (member
                for member in obj.__class__.members().itervalues()
                if isinstance(member, Slot))

    for slot in slots:
        blocks = obj.get(slot)
        if blocks is not None:
            for block in blocks:
                for descendant in find_blocks(block):
                    yield descendant

def add_block(block, parent, slot, positioning = "append", anchor = None):
    if isinstance(slot, schema.Reference):
        parent.set(slot, block)
    elif isinstance(slot, schema.Collection):
        collection = parent.get(slot)
        if positioning == "append":
            schema.add(collection, block)
        elif positioning == "before":
            collection.insert(collection.index(anchor), block)
        elif positioning == "after":
            collection.insert(collection.index(anchor) + 1, block)
        else:
            raise ValueError("Invalid block positioning: %s" % positioning)

def create_block_views(blocks):
    for block in blocks:
        if block.is_published():
            view = block.create_view()
            if view is not None:
                yield view

