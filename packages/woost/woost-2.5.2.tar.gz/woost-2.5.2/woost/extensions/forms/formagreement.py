#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item, Publishable


class FormAgreement(Item):

    type_group = "custom_forms"
    show_element_in_listing = False

    members_order = [
        "forms",
        "title",
        "document"
    ]

    forms = schema.Collection(
        items = "woost.extensions.forms.formblock.FormBlock",
        bidirectional = True,
        editable = False
    )

    title = schema.String(
        required = True,
        descriptive = True,
        translated = True,
        unique = True,
        indexed = True,
        normalized_index = True
    )

    document = schema.Reference(
        type = Publishable,
        related_end = schema.Collection()
    )

