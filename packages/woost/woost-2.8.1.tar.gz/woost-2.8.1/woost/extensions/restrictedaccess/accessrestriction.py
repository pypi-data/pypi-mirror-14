#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item


class AccessRestriction(Item):

    instantiable = True
    type_group = "users"

    members_order = [
        "title",
        "restricted_content"
    ]

    title = schema.String(
        translated = True,
        required = True,
        unique = True,
        indexed = True,
        spellcheck = True,
        descriptive = True
    )

    restricted_content = schema.Collection(
        items = "woost.models.Publishable",
        bidirectional = True,
        editable = schema.NOT_EDITABLE
    )

