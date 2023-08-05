#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail import schema
from cocktail.persistence import datastore
from cocktail.controllers import request_property, get_parameter
from woost.models import Item
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from woost.models import Block
from woost.models.blockutils import add_block
from woost.controllers.backoffice.editblockscontroller \
    import get_slot_parameter


class DropBlockController(BaseBackOfficeController):

    @request_property
    def block(self):
        return get_parameter(schema.Reference("block", type = Block))

    @request_property
    def source_parent(self):
        return get_parameter(schema.Reference("source_parent", type = Item))

    @request_property
    def source_slot(self):
        return get_slot_parameter(self.source_parent, "source_slot")

    @request_property
    def target_parent(self):
        return get_parameter(schema.Reference("target_parent", type = Item))

    @request_property
    def target_slot(self):
        return get_slot_parameter(self.target_parent, "target_slot")

    @request_property
    def anchor(self):
        return get_parameter(schema.Reference("anchor", type = Block))

    def __call__(self, **kwargs):

        block = self.block

        if block is None:
            raise cherrypy.HTTPError(400,
                "Must supply a 'block' parameter indicating the block to "
                "relocate"
            )

        source_parent = self.source_parent

        if source_parent is None:
            raise cherrypy.HTTPError(400,
                "Must supply a 'source_parent' parameter indicating the "
                "container that the block is being moved from"
            )

        source_slot = self.source_slot

        if source_slot is None:
            raise cherrypy.HTTPError(400,
                "Must supply a 'source_slot' parameter indicating the "
                "reference or collection that the block is being removed from"
            )

        target_parent = self.target_parent

        if target_parent is None:
            raise cherrypy.HTTPError(400,
                "Must supply a 'target_parent' parameter indicating the "
                "container that the block is being moved from"
            )

        target_slot = self.target_slot

        if target_slot is None:
            raise cherrypy.HTTPError(400,
                "Must supply a 'target_slot' parameter indicating the "
                "reference or collection that the block is being removed from"
            )

        anchor = self.anchor

        # Remove the block from its current position
        if isinstance(source_slot, schema.Reference):
            source_parent.set(source_slot, None)
        else:
            collection = source_parent.get(source_slot)
            schema.remove(collection, block)

        # Add it to its new location
        add_block(
            block,
            target_parent,
            target_slot,
            positioning = "append" if anchor is None else "before",
            anchor = anchor
        )

        datastore.commit()
        return ""

