#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from collections import Counter
from cocktail.translations import translations
from woost.models import Item, Configuration
from woost.controllers.notifications import Notification
from .state import TranslationWorkflowState

def get_models_included_in_translation_workflow(root_model = Item):
    return tuple(
        model
        for model in root_model.schema_tree()
        if model_is_included_in_translation_workflow(model)
    )

def model_is_included_in_translation_workflow(model):
    return (
        model.included_in_translation_workflow
        and any(
            member_is_included_in_translation_workflow(member)
            for member in model.iter_members()
        )
    )

def member_is_included_in_translation_workflow(member):
    return member.translated and member.included_in_translation_workflow

def object_is_included_in_translation_workflow(obj):
    return (
        obj.included_in_translation_workflow
        and isinstance(obj, get_models_included_in_translation_workflow())
    )

def iter_changeset_translation_requests(
    changeset,
    include_silenced = False,
    include_unchanged = False
):
    from .request import TranslationWorkflowRequest

    # Yield created or modified requests
    for change in changeset.changes.itervalues():
        if isinstance(change.target, TranslationWorkflowRequest):
            yield change.target

    # Yield silenced requests that would have been affected by the changeset
    if include_silenced or include_unchanged:
        silenced_state = TranslationWorkflowState.get_instance(
            qname = "woost.extensions.translationworkflow.states.silenced"
        )

        for item_id, change in changeset.changes.iteritems():
            if (
                change.action == "modify"
                and change.target
                and change.target.is_inserted
                and object_is_included_in_translation_workflow(change.target)
            ):
                source_languages = set()
                for member, language in change.diff():
                    if member_is_included_in_translation_workflow(member):
                        source_languages.add(language)

                language_paths = \
                    Configuration.instance.translation_workflow_paths

                for source_language in source_languages:
                    target_languages = language_paths.get(source_language)
                    if target_languages:
                        for target_language in target_languages:
                            request = change.target.get_translation_request(
                                source_language,
                                target_language
                            )
                            if request is not None:
                                if (
                                    (
                                        silenced_state is not None
                                        and request.state is silenced_state
                                    )
                                    or include_unchanged
                                ):
                                    yield request

def iter_changeset_translation_request_changes(
    changeset,
    include_silenced = False,
    include_unchanged = False,
    only_changed_states = False
):
    silenced_state = TranslationWorkflowState.get_instance(
        qname = "woost.extensions.translationworkflow.states.silenced"
    )

    for request in iter_changeset_translation_requests(changeset):
        request_change = changeset.changes.get(request.id)
        if request_change is None:
            if (
                silenced_state is not None
                and request.state is silenced_state
            ):
                if include_unchanged:
                    yield request, "silenced"
            elif include_unchanged:
                yield request, "unchanged"
        elif request_change.action == "create":
            yield request, "created",
        elif request_change.action == "modify":
            if (
                not only_changed_states
                or "state" in request_change.changed_members
            ):
                yield request, "invalidated"

def notify_translation_request_changes(changeset):

    silenced_count = 0
    state_count = Counter()

    for request, request_change \
    in iter_changeset_translation_request_changes(
        changeset,
        only_changed_states = True
    ):
        if request_change == "silenced":
            silenced_count += 1
        else:
            state_count[request.state] += 1

    for state, count in state_count.iteritems():
        Notification(
            translations(
                "woost.extensions.translationworkflow.transitions_notice",
                new_state = state,
                count = count
            ),
            "success"
        ).emit()

    if silenced_count:
        Notification(
            translations(
                "woost.extensions.translationworkflow.silence_notice",
                count = silenced_count
            )
        ).emit()

