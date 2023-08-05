#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2009
"""
from cocktail.translations import get_language
from cocktail import schema
from cocktail.controllers import get_parameter, request_property
from woost.models import Publishable, Block
from woost.controllers.backoffice.editcontroller import EditController
from woost.controllers.backoffice.useractions import get_user_action


class PreviewController(EditController):

    section = "preview"

    @request_property
    def previewed_item(self):
        return self.stack_node.item

    @request_property
    def preview_publishable(self):

        publishable = get_parameter(
            schema.Reference("preview_publishable",
                type = Publishable
            )
        )

        if publishable is not None:
            return publishable

        for node in reversed(self.edit_stack):
            item = getattr(node, "item", None)
            if item is not None and isinstance(item, Publishable):
                return item

        if isinstance(self.previewed_item, Block):
            for path in self.previewed_item.find_paths():
                container = path[0][0]
                if isinstance(container, Publishable):
                    return container

    @request_property
    def preview_language(self):
        return get_parameter(
            schema.String("preview_language",
                default = get_language()
            )
        )

    @request_property
    def view_class(self):
        return self.stack_node.item.preview_view

    @request_property
    def output(self):
        output = EditController.output(self)
        output.update(
            selected_action = get_user_action("preview"),
            previewed_item = self.previewed_item,
            preview_publishable = self.preview_publishable,
            preview_language = self.preview_language,
            item_translations = self.stack_node.item_translations
        )
        return output

