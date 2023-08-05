#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import cached_getter
from cocktail import schema
from cocktail.html import templates
from cocktail.html.uigeneration import display_factory
from cocktail.html.readonlydisplay import read_only_display
from woost.models import Item
from .path import TranslationWorkflowPath
from .transitionsetup import TranslationWorkflowTransitionSetup


class TranslationWorkflowAssignTransitionSetup(
    TranslationWorkflowTransitionSetup
):
    @cached_getter
    def multiple_choices(self):
        return any(
            len(translators) != 1
            for translators in self.eligible_translators.itervalues()
        )

    @cached_getter
    def transition_schema(self):

        transition_schema = schema.Schema(
            "woost.extensions.translationworkflow."
            "TranslationWorkflowAssignTransitionSetup"
        )

        def translator_edit_control(
            ui_generator,
            obj,
            member,
            value,
            **context
        ):
            selector = templates.new("cocktail.html.DropdownSelector")
            translation_path = context.get("item_key")
            if translation_path is not None:
                selector.items = \
                    self.eligible_translators.get(translation_path)
            return selector

        assignments = schema.Mapping("assignments",
            keys = TranslationWorkflowPath("translation_path",
                required = True,
                edit_control = read_only_display
            ),
            values = schema.Reference("translator",
                type = Item,
                required = True,
                # Limit the translator selection to translators who are able to
                # deal with each particular path
                enumeration = lambda ctx:
                    self.eligible_translators.get(ctx.collection_index),
                edit_control = translator_edit_control
            ),
            edit_control = display_factory(
                "cocktail.html.MappingEditor",
                fixed_entries = True
            )
        )

        # Make each path default to its first eligible translator
        assignments.default = {}

        for translation_path in self.translation_paths:
            path_translators = self.eligible_translators.get(translation_path)
            if path_translators:
                default_translator = path_translators[0]
            else:
                default_translator = None
            assignments.default[translation_path] = default_translator

        transition_schema.add_member(assignments)
        return transition_schema

