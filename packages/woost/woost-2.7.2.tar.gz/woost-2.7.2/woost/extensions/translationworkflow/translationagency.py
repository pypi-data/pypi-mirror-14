#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item, User
from .path import TranslationWorkflowPath


class TranslationAgency(Item):

    type_group = "users"

    members_order = [
        "title",
        "managers",
        "translators",
        "translation_proficiencies"
    ]

    title = schema.String(
        required = True,
        indexed = True,
        unique = True,
        descriptive = True
    )

    managers = schema.Collection(
        items = schema.Reference(type = User),
        bidirectional = True,
        related_key = "managed_translation_agency"
    )

    translators = schema.Collection(
        items = schema.Reference(type = User),
        bidirectional = True,
        related_key = "translation_agency"
    )

    translation_proficiencies = schema.Collection(
        items = TranslationWorkflowPath
    )

