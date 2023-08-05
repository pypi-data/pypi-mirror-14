#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item, File


class TranslationWorkflowState(Item):

    type_group = "translation_workflow"

    members_order = [
        "title",
        "plural_title",
        "color",
        "incomming_transitions",
        "outgoing_transitions"
    ]

    title = schema.String(
        translated = True,
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        descriptive = True,
        spellcheck = True
    )

    plural_title = schema.String(
        translated = True,
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        listed_by_default = False,
        spellcheck = True
    )

    color = schema.Color(
        required = True,
        default = "#ffffff",
        listed_by_default = False
    )

    incomming_transitions = schema.Collection(
        items = "woost.extensions.translationworkflow."
                "transition.TranslationWorkflowTransition",
        related_key = "target_state",
        bidirectional = True,
        cascade_delete = True
    )

    outgoing_transitions = schema.Collection(
        items = "woost.extensions.translationworkflow."
                "transition.TranslationWorkflowTransition",
        related_key = "source_states",
        bidirectional = True,
        cascade_delete = True
    )

    state_after_source_change = schema.Reference(
        items = schema.Reference(),
        listed_by_default = False
    )


# Self reference for state_after_source_change
TranslationWorkflowState.state_after_source_change.type = \
    TranslationWorkflowState

TranslationWorkflowState.state_after_source_change.related_end = \
    schema.Collection()

