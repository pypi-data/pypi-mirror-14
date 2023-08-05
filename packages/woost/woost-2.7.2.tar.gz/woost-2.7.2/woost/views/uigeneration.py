#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.html import templates
from cocktail.html.uigeneration import (
    UIGenerator,
    EditControlGenerator,
    default_display,
    default_edit_control,
    default_search_control
)
from woost.models import Item

# Custom read only display for the backoffice
#------------------------------------------------------------------------------
def _collection_backoffice_display(
    ui_generator,
    obj,
    member,
    value,
    **context
):
    if member.is_persistent_relation:
        return "woost.views.ContentList"

backoffice_display = UIGenerator(
    "backoffice_display",
    base_ui_generators = [default_display],
    member_type_displays = {
        Item: "woost.views.ItemDisplay",
        schema.Member: "cocktail.html.TranslationDisplay",
        schema.Collection: _collection_backoffice_display,
        schema.BaseDateTime: "cocktail.html.RelativeTimeDisplay"
    }
)

backoffice_read_only_control = UIGenerator(
    "backoffice_read_only_control",
    base_ui_generators = [backoffice_display]
)

# Display for the 'Element' column of backoffice listings
#------------------------------------------------------------------------------
backoffice_element_column_display = UIGenerator(
    base_ui_generators = [backoffice_display],
    member_type_displays = {
        Item: "woost.views.ItemLabel"
    }
)

# Custom editable display for the backoffice
#------------------------------------------------------------------------------
def _collection_backoffice_edit_control(
    ui_generator,
    obj,
    member,
    value,
    **context
):
    if member.is_persistent_relation:
        return "woost.views.ItemCollectionEditor"
    else:
        return "cocktail.html.CollectionEditor"

def _reference_backoffice_edit_control(
    ui_generator,
    obj,
    member,
    value,
    **context
):
    if member.class_family is not None:
        display = templates.new("woost.views.Autocomplete")
        display.ajax_search = False
        display.show_types = False
        return display
    else:
        return "woost.views.ItemSelector"

backoffice_edit_control = EditControlGenerator(
    "backoffice_edit_control",
    base_ui_generators = [default_edit_control],
    member_type_displays = {
        schema.Collection: _collection_backoffice_edit_control,
        schema.Reference: _reference_backoffice_edit_control,
        schema.HTML: "woost.views.RichTextEditor"
    }
)

backoffice_edit_control.read_only_ui_generator = backoffice_read_only_control

# Custom selection controls for the item selector
#------------------------------------------------------------------------------
backoffice_selection_control = UIGenerator(
    "backoffice_selection_control",
    member_type_displays = {
        schema.Reference: "woost.views.Autocomplete"
    }
)

backoffice_integral_selection_control = UIGenerator(
    "backoffice_integral_selection_control",
    base_ui_generators = [backoffice_display]
)

# Custom search controls for the backoffice
#------------------------------------------------------------------------------
def _reference_backoffice_search_control(
    ui_generator,
    obj,
    member,
    value,
    **context
):
    if member.class_family is None and member.related_type is not None:
        display = templates.new("woost.views.Autocomplete")
        display.ajax_search_threshold = None
        member_schema = member.original_member.schema
        if not isinstance(member_schema, type) or not member_schema.__module__:
            display.ajax_url = (
                "/autocomplete/%s/QUERY"
                % member.related_type.get_qualified_name(include_ns = True)
            )
        return display

backoffice_search_control = EditControlGenerator(
    "backoffice_search_control",
    base_ui_generators = [
        default_search_control,
        backoffice_edit_control
    ],
    member_type_displays = {
        schema.Reference: _reference_backoffice_search_control
    }
)

