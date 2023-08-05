#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import when
from cocktail import schema
from woost.models import Item, Configuration
from woost.extensions.translationworkflow.request \
    import TranslationWorkflowRequest
from .utils import (
    get_models_included_in_translation_workflow,
    object_is_included_in_translation_workflow,
    member_is_included_in_translation_workflow
)

Item.translation_workflow_request_class = TranslationWorkflowRequest

Item.add_member(
    schema.Collection("translation_requests",
        items = "woost.extensions.translationworkflow."
                "request.TranslationWorkflowRequest",
        bidirectional = True,
        integral = True,
        editable = schema.READ_ONLY,
        backoffice_read_only_control =
            "woost.extensions.translationworkflow."
            "TranslationWorkflowRequestCollectionEditor",
        member_group = "administration"
    )
)

def get_translation_request(self, source_language, target_language):

    for request in self.translation_requests:
        if (
            request.source_language == source_language
            and request.target_language == target_language
        ):
            return request

    return None

Item.get_translation_request = get_translation_request

def require_translation_request(self, source_language, target_language):
    request = self.get_translation_request(source_language, target_language)
    if request is None:
        request = self.translation_workflow_request_class()
        request.translated_item = self
        request.source_language = source_language
        request.target_language = target_language
    return request

Item.require_translation_request = require_translation_request

REQUIRE_ALL = 1
REQUIRE_MISSING_TRANSLATIONS = 2
REQUIRE_OUTDATED_TRANSLATIONS = 3

@classmethod
def require_all_translation_requests(
    cls,
    language_paths = None,
    policy = REQUIRE_MISSING_TRANSLATIONS,
    state = None,
    subset = None,
    verbose = False
):
    if language_paths is None:
        language_paths = Configuration.instance.translation_workflow_paths

    models = get_models_included_in_translation_workflow()

    if not models:
        return []

    if verbose:
        print "Considering the following models:"
        for model in models:
            print " - ", model.__name__

    if subset is None:
        subset = cls.select()

    for instance in subset:

        if not isinstance(instance, models):
            continue

        if verbose:
            printed_heading = False

        for source_language, target_languages in language_paths.iteritems():
            if source_language in instance.translations:
                for target_language in target_languages:
                    if policy == REQUIRE_MISSING_TRANSLATIONS:
                        if target_language in instance.translations:
                            continue
                    elif policy == REQUIRE_OUTDATED_TRANSLATIONS:
                        source_date = instance.get(
                            "last_translation_update_time",
                            source_language
                        )
                        target_date = instance.get(
                            "last_translation_update_time",
                            target_language
                        )
                        if trans_date is not None \
                        and target_date >= source_date:
                            continue

                    request = instance.require_translation_request(
                        source_language,
                        target_language
                    )

                    is_new_request = request.insert()

                    if state is not None and is_new_request:
                        request.state = state

                    if verbose and is_new_request:
                        if not printed_heading:
                            print
                            print instance
                            printed_heading = True
                        print u"  %s -> %s" % (
                            source_language,
                            target_language
                        )

Item.require_all_translation_requests = require_all_translation_requests

def invalidate_translation_request(self, source_language, target_language):
    request = self.require_translation_request(
        source_language,
        target_language
    )
    if not request.insert():
        new_state = request.state.state_after_source_change
        if new_state is not None:
            # TODO: notify the assigned translator
            # ("The source text for the translation you were working on has
            #   changed and the translation request has been pulled back")
            request.state = new_state

Item.invalidate_translation_request = invalidate_translation_request

schema.Member.included_in_translation_workflow = True
schema.SchemaObject.included_in_translation_workflow = False
Item.last_translation_update_time.included_in_translation_workflow = False

@when(Item.inserted)
def generate_translation_requests_for_new_item(e):
    if object_is_included_in_translation_workflow(e.source):
        for member in e.source.__class__.iter_members():
            if member_is_included_in_translation_workflow(member):
                language_paths = Configuration.instance.translation_workflow_paths
                for source_language in e.source.translations:
                    target_languages = language_paths.get(source_language)
                    if target_languages:
                        for target_language in target_languages:
                            request = e.source.translation_workflow_request_class()
                            request.translated_item = e.source
                            request.source_language = source_language
                            request.target_language = target_language
                            request.insert()

@when(Item.changed)
def update_translation_requests_for_modified_item(e):
    if (
        e.source.is_inserted
        and object_is_included_in_translation_workflow(e.source)
        and member_is_included_in_translation_workflow(e.member)
        and e.value
    ):
        language_paths = Configuration.instance.translation_workflow_paths
        target_languages = language_paths.get(e.language)
        if target_languages:
            for target_language in target_languages:
                e.source.invalidate_translation_request(
                    e.language,
                    target_language
                )

