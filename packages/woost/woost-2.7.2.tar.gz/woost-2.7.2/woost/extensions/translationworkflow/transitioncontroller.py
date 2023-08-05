#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import event_handler
from cocktail.pkgutils import resolve
from cocktail.translations import translations
from cocktail import schema
from cocktail.controllers import (
    FormProcessor,
    Form,
    request_property
)
from woost import app
from woost.models import changeset_context
from woost.controllers.notifications import Notification
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from .transitionpermission import TranslationWorkflowTransitionPermission


class TranslationWorkflowTransitionController(
    FormProcessor,
    BaseBackOfficeController
):
    is_transactional = True
    view_class = (
        "woost.extensions.translationworkflow."
        "TranslationWorkflowTransitionView"
    )

    @event_handler
    def handle_before_request(cls, e):
        controller = e.source
        transition = controller.transition
        user = app.user
        for request in controller.requests:
            user.require_permission(
                TranslationWorkflowTransitionPermission,
                translation_request = request,
                transition = transition
            )

    @request_property
    def requests(self):
        return self.stack_node.requests

    @request_property
    def transition(self):
        return self.stack_node.transition

    class TransitionForm(Form):

        @request_property
        def transition_setup(self):
            return (
                resolve(self.controller.transition.transition_setup_class)
                (self.controller.transition, self.controller.requests)
            )

        @request_property
        def schema(self):
            return self.transition_setup.transition_schema

        def submit(self):
            Form.submit(self)

            transition = self.controller.transition
            transition_data = self.data

            with changeset_context(author = app.user) as changeset:
                for request in self.controller.requests:
                    transition.execute(request, transition_data)
                    changeset.changes[request.id].is_explicit_change = True

        def after_submit(self):
            Notification(
                translations(
                    "woost.extensions.translationworkflow."
                    "transition_executed_notice",
                    transition = self.controller.transition,
                    requests = self.controller.requests
                ),
                "success"
            ).emit()
            self.controller.go_back()

    @request_property
    def output(self):
        output = BaseBackOfficeController.output(self)
        output["requests"] = self.requests
        output["transition"] = self.transition
        return output

