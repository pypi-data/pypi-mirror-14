#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			June 2008
"""
from cocktail import schema
from woost.models import Item


class Template(Item):

    type_group = "customization"

    members_order = [
        "title",
        "identifier",
        "documents"
    ]

    title = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True
    )

    identifier = schema.String(
        required = True,
        unique = True,
        indexed = True,
        max = 255,
        text_search = False
    )

    documents = schema.Collection(
        items = "woost.models.Document",
        bidirectional = True,
        editable = False,
        synchronizable = False,
        visible_in_reference_list = False
    )

