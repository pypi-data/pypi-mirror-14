#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Role
from .state import TranslationWorkflowState
from .transition import TranslationWorkflowTransition

Role.add_member(
    schema.Collection("translation_workflow_relevant_states",
        items = schema.Reference(
            type = TranslationWorkflowState
        ),
        related_end = schema.Collection()
    ),
    append = True
)

Role.add_member(
    schema.Reference("translation_workflow_default_state",
        type = TranslationWorkflowState,
        related_end = schema.Collection(),
        enumeration = Role.translation_workflow_relevant_states,
        listed_by_default = False
    ),
    append = True
)

Role.add_member(
    schema.Reference("translation_workflow_default_transition",
        type = TranslationWorkflowTransition,
        related_end = schema.Collection(),
        listed_by_default = False
    ),
    append = True
)

Role.add_member(
    schema.CodeBlock("translation_workflow_default_transition_condition",
        language = "python",
        listed_by_default = False
    ),
    append = True
)

