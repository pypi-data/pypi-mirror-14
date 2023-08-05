#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import User, LocaleMember
from .path import TranslationWorkflowPath
from .translationagency import TranslationAgency

User.members_order += [
    "managed_translation_agency",
    "translation_agency",
    "translation_proficiencies"
]

User.add_member(
    schema.Reference("managed_translation_agency",
        type = TranslationAgency,
        bidirectional = True,
        related_key = "managers",
        editable = schema.READ_ONLY,
        listed_by_default = False
    )
)

User.add_member(
    schema.Reference("translation_agency",
        type = TranslationAgency,
        bidirectional = True,
        related_key = "translators",
        editable = schema.READ_ONLY,
        indexed = True,
        listed_by_default = False
    )
)

User.add_member(
    schema.Collection("translation_proficiencies",
        items = TranslationWorkflowPath
    )
)

