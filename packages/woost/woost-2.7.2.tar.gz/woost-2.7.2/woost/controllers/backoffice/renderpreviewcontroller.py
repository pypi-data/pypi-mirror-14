#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
import cherrypy
from simplejson import dumps
from cocktail.translations import translations, get_language, set_language
from cocktail import schema
from cocktail.controllers import get_parameter, request_property
from cocktail.html import Element, templates
from woost import app
from woost.models import ReadPermission, Publishable
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController


class RenderPreviewController(BaseBackOfficeController):

    @request_property
    def previewed_item(self):
        return self.stack_node.item

    @request_property
    def preview_publishable(self):
        return get_parameter(
            schema.Reference("preview_publishable",
                type = Publishable
            )
        )

    @request_property
    def preview_language(self):
        return get_parameter(
            schema.String("preview_language",
                default = get_language()
            )
        )

    def __call__(self, *args, **kwargs):

        node = self.stack_node
        previewed_item = self.previewed_item
        publishable = self.preview_publishable
        preview_language = self.preview_language
        user = app.user

        # Set the language for the preview
        if preview_language:
            set_language(preview_language)

        # Enforce permissions
        user.require_permission(ReadPermission, target = previewed_item)

        if publishable is not previewed_item:
            user.require_permission(ReadPermission, target = publishable)

        # Disable the preview if the item's unsaved state produces validation
        # errors; these would usually lead to unhandled server errors during
        # rendering.
        errors = schema.ErrorList(node.iter_errors())

        if errors:
            error_box = templates.new("cocktail.html.ErrorBox")
            error_box.errors = errors
            message = Element("div",
                class_name = "preview-error-box",
                children = [
                    translations(
                        "woost.backoffice invalid item preview",
                        preview_language
                    ),
                    error_box
                ]
            )
            message.add_resource("/resources/styles/backoffice.css")
            return message.render_page()

        # Update the edited item with the data to preview
        node.import_form_data(node.form_data, previewed_item)

        app.original_publishable = app.publishable
        app.publishable = publishable

        controller = publishable.resolve_controller()

        if controller is None:
            raise cherrypy.NotFound()

        if isinstance(controller, type):
            controller = controller()

        return controller()

