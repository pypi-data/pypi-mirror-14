#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.controllers import context
from woost.controllers.backoffice.editstack import StackNode
from .transition import TranslationWorkflowTransition
from .request import TranslationWorkflowRequest


class TranslationWorkflowTransitionNode(StackNode):

    requests = None
    transition = None

    def __getstate__(self):

        state = {}

        for key, value in self.__dict__.iteritems():
            if key == "requests":
                value = [request.id for request in value]
            elif key == "transition":
                value = value.id
            state[key] = value

        return state

    def __setstate__(self, state):

        for key, value in state.iteritems():
            if key == "requests":
                value = filter(None, [
                    TranslationWorkflowRequest.get_instance(id)
                    for id in value
                ])
            elif key == "transition":
                value = TranslationWorkflowTransition.get_instance(value)

            setattr(self, key, value)

    def uri(self, **params):

        if "edit_stack" not in params:
            params["edit_stack"] = self.stack.to_param(self.index)

        return context["cms"].contextual_uri(
            "translation_workflow_transition", **params
        )

