#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail.events import event_handler
from cocktail import schema
from cocktail.controllers import request_property, get_parameter
from woost.models import Item
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from woost.models import Block
from woost.controllers.backoffice.editstack import EditBlocksNode


class EditBlocksController(BaseBackOfficeController):

    view_class = "woost.views.EditBlocksView"

    @event_handler
    def handle_before_request(cls, e):
        controller = e.source

        if not isinstance(controller.stack_node, EditBlocksNode):
            edit_stack = controller.edit_stack
            edit_stacks_manager = controller.context["edit_stacks_manager"]

            if edit_stack is None:
                edit_stack = edit_stacks_manager.create_edit_stack()
                edit_stacks_manager.current_edit_stack = edit_stack

            node = EditBlocksNode()
            node.item = controller.edited_item
            edit_stack.push(node)
            edit_stacks_manager.preserve_edit_stack(edit_stack)
            edit_stack.go()

    def resolve(self, path):

        try:
            self.edited_item = Item.require_instance(int(path.pop(0)))
        except:
            raise cherrypy.HTTPError(400)

        return self

    @request_property
    def submitted(self):
        return cherrypy.request.method == "POST"

    def submit(self):
        self._invoke_user_action(
            self._get_user_action(),
            [self.block or self.block_parent or self.edited_item]
        )

    @request_property
    def block(self):
        return get_parameter(schema.Reference("block", type = Block))

    @request_property
    def block_parent(self):
        return get_parameter(schema.Reference("block_parent", type = Item))

    @request_property
    def block_slot(self):
        return get_slot_parameter(self.block_parent, "block_slot")

    @request_property
    def output(self):
        output = BaseBackOfficeController.output(self)
        output.update(
            edited_item = self.edited_item
        )
        return output


def get_slot_parameter(parent, parameter_name):
    if parent is not None:
        slot_name = get_parameter(schema.String(parameter_name))
        if slot_name:
            slot = type(parent).get_member(slot_name)
            if (
                slot is not None
                and isinstance(slot, schema.RelationMember)
                and slot.related_type
                and issubclass(slot.related_type, Block)
            ):
                return slot

