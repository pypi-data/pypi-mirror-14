#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import cached_getter
from woost.models import User, get_current_user
from .translationagency import TranslationAgency


class TranslationWorkflowTransitionSetup(object):

    def __init__(self, transition, requests):
        self.transition = transition
        self.requests = requests

    @cached_getter
    def multiple_choices(self):
        return True

    @cached_getter
    def transition_schema(self):
        return None

    @cached_getter
    def translation_paths(self):
        return set(
            (request.source_language, request.target_language)
            for request in self.requests
        )

    @cached_getter
    def eligible_translators(self):

        user = get_current_user()
        agency = user.managed_translation_agency

        # Coordinators can assign to freelance translators and to translation
        # agencies
        if agency is None:
            all_translators = (
                list(TranslationAgency.select())
                + list(User.select({
                    "enabled": True,
                    "translation_agency": None
                }))
            )
        # Translation agency managers can assign to their agency's translators
        else:
            all_translators = agency.translators

        # Filter translators / agencies by language proficiencies
        return dict(
            (translation_path, [
                translator
                for translator in all_translators
                if translation_path in translator.translation_proficiencies
            ])
            for translation_path in self.translation_paths
        )

