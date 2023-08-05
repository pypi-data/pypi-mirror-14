#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
from cocktail.events import event_handler
from cocktail import schema
from cocktail.modeling import getter
from .item import Item


class Style(Item):

    type_group = "customization"

    members_order = [
        "title",
        "applicable_to_text",
        "applicable_to_blocks",
        "custom_class_name",
        "html_tag",
        "editor_keyboard_shortcut",
        "declarations",
        "admin_declarations"
    ]

    title = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        spellcheck = True
    )

    applicable_to_text = schema.Boolean(
        required = True,
        indexed = True,
        default = True,
        listed_by_default = False
    )

    applicable_to_blocks = schema.Boolean(
        required = True,
        default = True,
        indexed = True,
        listed_by_default = False
    )

    custom_class_name = schema.String(
        indexed = True,
        unique = True,
        normalized_index = False,
        listed_by_default = False
    )

    html_tag = schema.String(
        listed_by_default = False
    )

    editor_keyboard_shortcut = schema.String(
        listed_by_default = False
    )

    declarations = schema.String(
        text_search = False,
        edit_control = "cocktail.html.TextArea",
        listed_by_default = False
    )

    admin_declarations = schema.String(
        text_search = False,
        edit_control = "cocktail.html.TextArea",
        listed_by_default = False
    )

    @property
    def class_name(self):
        return self.custom_class_name or ("woost_style_%d" % self.id)

