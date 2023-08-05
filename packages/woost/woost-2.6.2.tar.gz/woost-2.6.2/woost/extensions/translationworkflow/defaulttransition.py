#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.controllers import get_parameter
from woost.models import get_current_user
from .transition import TranslationWorkflowTransition
from .transitionpermission import TranslationWorkflowTransitionPermission
from .utils import iter_changeset_translation_requests

def apply_default_transition(e):

    if e.change is None:
        return

    if not get_parameter(
        schema.Boolean("translation_workflow_auto_transition")
    ):
        return

    user = get_current_user()

    if user is None:
        return

    transition = None
    condition = None

    for role in user.iter_roles():
        if role.translation_workflow_default_transition:
            transition = role.translation_workflow_default_transition
            if role.translation_workflow_default_transition_condition:
                condition = compile(
                    role.translation_workflow_default_transition_condition,
                    "%s #%s.translation_workflow_default_transition_condition" % (
                        role.__class__.__name__,
                        role.id
                    ),
                    "exec"
                )
            break

    if transition is None:
        return

    for request in list(
        iter_changeset_translation_requests(
            e.change.changeset,
            include_unchanged = True
        )
    ):
        if (
            (
                not transition.source_states
                or request.state in transition.source_states
            )
            and user.has_permission(
                TranslationWorkflowTransitionPermission,
                transition = transition,
                translation_request = request
            )
        ):
            if condition is not None:
                context = {
                    "request": request,
                    "transition": transition,
                    "applies": True
                }
                exec condition in context
                if not context["applies"]:
                    continue
            transition.execute(request)

