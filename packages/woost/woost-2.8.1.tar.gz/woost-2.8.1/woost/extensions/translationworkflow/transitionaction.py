#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail.translations import translations
from cocktail.pkgutils import resolve
from cocktail import schema
from cocktail.persistence import transaction
from cocktail.controllers import request_property, context, Location
from woost import app
from woost.models import changeset_context, ModifyPermission
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from woost.controllers.backoffice.useractions import (
    UserAction,
    get_user_action
)
from .request import TranslationWorkflowRequest
from .transitionpermission import TranslationWorkflowTransitionPermission
from .transitionnode import TranslationWorkflowTransitionNode
from .utils import (
    member_is_included_in_translation_workflow,
    notify_translation_request_changes
)


class TranslationWorkflowTransitionAction(UserAction):

    content_type = TranslationWorkflowRequest
    min = 1
    max = None
    included = frozenset([
        "toolbar",
        "item_buttons"
    ])
    show_as_primary_action = "on_content_type"
    hidden_when_disabled = True
    _transition_id = None

    def __translate__(self, language, **kwargs):
        return translations(self.transition, language, **kwargs)

    @request_property
    def transition(self):
        from .transition import TranslationWorkflowTransition
        return TranslationWorkflowTransition.get_instance(self._transition_id)

    @request_property
    def icon_uri(self):
        icon = self.transition.icon
        return (
            icon
            and icon.get_uri()
            or "/resources/images/translation_workflow_transition.png"
        )

    def is_available(self, context, target):

        if isinstance(target, TranslationWorkflowRequest):
            transition = self.transition

            if (
                transition.requires_different_state
                and target.state is transition.target_state
            ):
                return False

            if (
                transition.source_states
                and target.state not in transition.source_states
            ):
                return False

        return UserAction.is_available(self, context, target)

    def is_permitted(self, user, target):
        return user.has_permission(
            TranslationWorkflowTransitionPermission,
            translation_request = None if isinstance(target, type) else target,
            transition = self.transition
        )

    def invoke(self, controller, selection):

        transition_data = None
        user = app.user

        # Save the edit stack
        if (
            len(selection) == 1
            and controller.edit_node
            and isinstance(
                controller.edit_node.item,
                TranslationWorkflowRequest
            )
            and hasattr(controller, "save_item")
            and user.has_permission(
                ModifyPermission,
                target = selection[0]
            )
        ):
            try:
                controller.save_item()
            except cherrypy.HTTPRedirect:
                pass

        # Initialize the transition process. If the transition requires
        # parameters, spawn a new node in the edit stack and redirect the user
        # to a form.
        if self.transition.transition_setup_class:
            transition_setup = (
                resolve(self.transition.transition_setup_class)
                (self.transition, selection)
            )
            if transition_setup.multiple_choices:
                node = TranslationWorkflowTransitionNode()
                node.requests = selection
                node.transition = self.transition
                node.push_to_stack()
                node.go()

            transition_schema = transition_setup.transition_schema
            if transition_schema is not None:
                transition_data = {}
                transition_schema.init_instance(transition_data)

        # Otherwise, execute the transition right away
        def execute_transition():
            transition = self.transition
            with changeset_context(author = user) as changeset:
                for request in selection:
                    transition.execute(request, transition_data)
                    change = changeset.changes.get(request.id)
                    if change is not None:
                        change.is_explicit_change = True
            return changeset

        changeset = transaction(execute_transition)
        notify_translation_request_changes(changeset)
        Location.get_current().go("GET")

    def get_errors(self, controller, selection):

        for error in UserAction.get_errors(self, controller, selection):
            yield error

        # Some transitions (ie. "apply") can't proceed unless the text in the
        # request is complete and valid
        if self.transition.requires_valid_text:
            stack_node = getattr(controller, "stack_node", None)

            # Applying the transition on a request that is being edited:
            # validate the edit state
            if stack_node is not None and selection == [stack_node.item]:
                adapter = schema.Adapter()
                adapter.implicit_copy = False
                for member in stack_node.form_schema.iter_members():
                    if member.name.startswith("translated_values_"):
                        adapter.copy(
                            member.name,
                            properties = {"required": True}
                        )
                val_schema = adapter.export_schema(stack_node.form_schema)
                for error in val_schema.get_errors(
                    stack_node.form_data,
                    languages = stack_node.item_translations,
                    persistent_object = stack_node.item
                ):
                    yield TranslationWorkflowInvalidTextError(
                        stack_node.item,
                        self.transition,
                        error
                    )

            # Applying the transition outside an edit form
            else:
                val_schemas = {}

                for request in selection:
                    translated_model = request.translated_item.__class__
                    val_schema = val_schemas.get(translated_model)

                    if val_schema is None:
                        adapter = schema.Adapter()
                        adapter.implicit_copy = False
                        for member in translated_model.iter_members():
                            if member_is_included_in_translation_workflow(member):
                                adapter.copy(
                                    member.name,
                                    properties = {
                                        "required": True,
                                        "translated": False
                                    }
                                )
                        val_schema = adapter.export_schema(translated_model)
                        val_schemas[translated_model] = val_schema

                    for error in val_schema.get_errors(
                        request.translated_values
                    ):
                        yield TranslationWorkflowInvalidTextError(
                            request,
                            self.transition,
                            error
                        )

    @classmethod
    def register_transition_action(cls, transition):
        action = cls.get_transition_action(transition)
        if action is None:
            action = cls("translation_workflow_transition_%d" % transition.id)
            action._transition_id = transition.id
            action.register()

    @classmethod
    def get_transition_action(cls, transition):
        return get_user_action(
            "translation_workflow_transition_%d" % transition.id
        )


class TranslationWorkflowInvalidTextError(Exception):

    def __init__(self, request, transition, error):
        self.request = request
        self.transition = transition
        self.error = error


BaseBackOfficeController._graceful_user_action_errors.add(
    TranslationWorkflowInvalidTextError
)

