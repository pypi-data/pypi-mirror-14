#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import Event, event_handler
from cocktail.translations import translations
from cocktail import schema
from cocktail.persistence import datastore
from cocktail.controllers import request_property
from woost.models import Item, File


class TranslationWorkflowTransition(Item):

    type_group = "translation_workflow"
    visible_from_root = False

    executed = Event(
        """An event triggered when the transaction is executed."""
    )

    members_order = [
        "title",
        "source_states",
        "target_state",
        "icon",
        "relative_order",
        "requires_valid_text",
        "requires_different_state",
        "transition_setup_class",
        "transition_code"
    ]

    title = schema.String(
        required = True,
        translated = True,
        descriptive = True,
        spellcheck = True
    )

    source_states = schema.Collection(
        items = "woost.extensions.translationworkflow."
               "state.TranslationWorkflowState",
        bidirectional = True,
        related_key = "outgoing_transitions"
    )

    target_state = schema.Reference(
        type = "woost.extensions.translationworkflow."
               "state.TranslationWorkflowState",
        bidirectional = True,
        related_key = "incomming_transitions"
    )

    icon = schema.Reference(
        type = File,
        relation_constraints = {"resource_type": "image"},
        related_end = schema.Collection(),
        listed_by_default = False
    )

    relative_order = schema.Integer(
        default = 0,
        indexed = True
    )

    requires_valid_text = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False
    )

    requires_different_state = schema.Boolean(
        required = True,
        default = True,
        listed_by_default = False
    )

    transition_setup_class = schema.String(
        listed_by_default = False
    )

    transition_code = schema.CodeBlock(
        language = "python",
        listed_by_default = False
    )

    def get_representative_image(self, icon_factory = None):
        return self.icon

    def execute(self, request, data = None):

        previous_state = request.state
        request.state = self.target_state

        if self.transition_code:
            label = "%r transition_code" % self
            code = compile(self.transition_code, label, "exec")
            exec code in {
                "transition": self,
                "request": request,
                "previous_state": previous_state,
                "data": data
            }

        if request.state is None:
            raise TransitionWithNoTargetStateError(self, request)

        self.executed(request = request, data = data)


class TransitionWithNoTargetStateError(Exception):

    def __init__(self, transition, request):
        self.transition = transition
        self.request = request
        Exception.__init__(
            self,
            u"%r failed to select a target state for %r"
            % (transition, request)
        )

