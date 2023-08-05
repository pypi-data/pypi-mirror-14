#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2008
"""
from cocktail.modeling import extend, call_base
from cocktail.translations import translations, require_language
from cocktail.html import Element, templates
from cocktail.html.hiddeninput import HiddenInput
from woost.models import (
    Item,
    Publishable,
    CreatePermission,
    ModifyPermission,
    DeletePermission,
    get_current_user
)
from woost.views.uigeneration import (
    backoffice_selection_control,
    backoffice_integral_selection_control
)


class ItemSelector(Element):

    existing_items_only = False
    selection_ui_generator = backoffice_selection_control
    integral_selection_ui_generator = backoffice_integral_selection_control
    descriptive_member = None
    descriptive_member_language = None

    def _build(self):

        Element._build(self)

        self.selection_wrapper = self.create_selection_wrapper()
        self.append(self.selection_wrapper)

        self.buttons = self.create_buttons()
        self.append(self.buttons)

    def _binding(self):
        if self.member is not None:
            self.selection_display = self.create_selection_display()
            self.selection_wrapper.append(self.selection_display)
            self.data_binding_delegate = self.selection_display

    def _ready(self):

        Element._ready(self)

        if (
            self.descriptive_member is None
            and self.member
            and self.member.related_type
        ):
            self.descriptive_member = \
                self.member.related_type.descriptive_member

        if self.descriptive_member:
            self.add_resource("/resources/scripts/ItemSelector.js")

            key = self.descriptive_member.name
            if self.descriptive_member.translated:
                key += "-" + require_language(self.descriptive_member_language)

            self.set_client_param("descriptiveMember", key)

        if self.member:

            user = get_current_user()

            # New
            if (
                not self.existing_items_only
                and any(
                    user.has_permission(CreatePermission, target = cls)
                    for cls in self.member.type.schema_tree()
                )
            ):
                self.new_button = self.create_new_button()
                self.buttons.append(self.new_button)

            # Select
            if self.existing_items_only or not self.member.integral:
                self.select_button = self.create_select_button()
                self.buttons.append(self.select_button)

            if not self.existing_items_only:

                # Edit
                if any(
                    user.has_permission(ModifyPermission, target = cls)
                    for cls in self.member.type.schema_tree()
                ):
                    self.edit_button = self.create_edit_button()
                    self.buttons.append(self.edit_button)

                # Delete
                if self.member.integral:
                    if any(
                        user.has_permission(DeletePermission, target = cls)
                        for cls in self.member.type.schema_tree()
                    ):
                        self.delete_button = self.create_delete_button()
                        self.buttons.append(self.delete_button)

        if self.value is None:
            self.add_class("empty_selection")

    def create_selection_wrapper(self):
        selection_wrapper = Element()
        selection_wrapper.add_class("selection_wrapper")
        return selection_wrapper

    def create_selection_display(self):

        if self.member.integral:
            ui_generator = self.integral_selection_ui_generator
        else:
            ui_generator = self.selection_ui_generator

        selection_display = ui_generator.create_member_display(
            self.data,
            self.member,
            self.value
        )
        selection_display.add_class("selection_display")

        # Displays for integral relations will typically be read only; add a
        # hidden input to hold their value if required.
        if self.member.integral:
            element = selection_display
            while element.data_binding_delegate is not None:
                element = element.data_binding_delegate
            if not element.is_form_control:
                hidden_input = HiddenInput()
                selection_display.append(hidden_input)
                selection_display.data_binding_delegate = hidden_input

        return selection_display

    def create_buttons(self):
        buttons = Element()
        buttons.add_class("ItemSelector-buttons")
        return buttons

    def create_select_button(self):

        select_button = Element("button",
            name = "relation-select",
            type = "submit",
            class_name = "ItemSelector-button select",
            value = self.member.type.full_name + "-" + self.name
        )
        select_button.append(
            translations("woost.views.ItemSelector select")
        )
        return select_button

    def create_unlink_button(self):

        unlink_button = Element("button",
            name = "relation-unlink",
            type = "submit",
            class_name = "ItemSelector-button unlink",
            value = self.member.name
        )
        unlink_button.append(
            translations("woost.views.ItemSelector unlink")
        )
        return unlink_button

    def create_new_button(self):

        new_button = Element(class_name = "ItemSelector-button new")

        instantiable_types = set(
            content_type
            for content_type in (
                [self.member.type] + list(self.member.type.derived_schemas())
            )
            if content_type.visible
            and content_type.instantiable
            and get_current_user().has_permission(
                CreatePermission,
                target = content_type
            )
        )

        if len(instantiable_types) > 1:

            new_button.add_class("selector")
            label = Element("span", class_name = "label")
            new_button.append(label)

            container = Element(class_name = "selector_content")
            new_button.append(container)

            content_type_tree = templates.new("woost.views.ContentTypeTree")
            content_type_tree.root = self.member.type
            content_type_tree.filter_item = instantiable_types.__contains__

            @extend(content_type_tree)
            def create_label(tree, content_type):
                label = call_base(content_type)
                label.tag = "button"
                label["type"] = "submit"
                label["name"] = "relation-new"
                label["value"] = self.member.name + "-" + content_type.full_name
                return label

            container.append(content_type_tree)
        else:
            new_button.tag = "button"
            new_button["type"] = "submit"
            new_button["name"] = "relation-new"
            new_button["value"] = \
                self.member.name + "-" + list(instantiable_types)[0].full_name
            label = new_button

        label.append(translations("woost.views.ItemSelector new"))

        return new_button

    def create_edit_button(self):

        edit_button = Element("button",
            name = "relation-edit",
            type = "submit",
            class_name = "ItemSelector-button edit",
            value = self.member.name
        )
        edit_button.append(
            translations("woost.views.ItemSelector edit")
        )
        return edit_button

    def create_delete_button(self):

        delete_button = Element("button",
            name = "relation-unlink",
            type = "submit",
            class_name = "ItemSelector-button delete",
            value = self.member.name
        )
        delete_button.append(
            translations("woost.views.ItemSelector delete")
        )
        return delete_button

