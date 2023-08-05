#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2014
"""
from cocktail.modeling import cached_getter
from cocktail.stringutils import normalize
from cocktail.translations import translations, descend_language_tree
from cocktail.html.datadisplay import display_factory
from woost.models import Configuration
from woost.models.enabledtranslations import (
    auto_enable_translations,
    auto_disable_translations
)
from woost.controllers.backoffice.editstack import EditNode


class EnabledTranslationsEditNode(EditNode):

    @cached_getter
    def form_schema(self):
        form_schema = EditNode.form_schema(self)

        enabled_translations = form_schema.get_member("enabled_translations")
        if enabled_translations is not None:
            enabled_translations.items.enumeration = \
                lambda ctx: self._enabled_translations_enumeration(ctx)
            enabled_translations.edit_control = display_factory(
                "woost.views.EnabledTranslationsSelector",
                defined_translations = self.item_translations
            )

        return form_schema

    def _enabled_translations_enumeration(self, ctx):
        eligible_languages = set()

        for language in self.item_translations:
            eligible_languages.update(descend_language_tree(language))

        eligible_languages.difference_update(
            Configuration.instance.virtual_languages
        )

        return sorted(
            list(eligible_languages),
            key = lambda language:
                normalize(translations("locale", locale = language))
        )

    def add_translation(self, language):
        EditNode.add_translation(self, language)
        enabled_translations = self.form_data.get("enabled_translations")
        if enabled_translations is not None:
            auto_enable_translations(
                language,
                self.item_translations,
                enabled_translations
            )

    def remove_translation(self, language):
        EditNode.remove_translation(self, language)
        enabled_translations = self.form_data.get("enabled_translations")
        if enabled_translations is not None:
            auto_disable_translations(
                language,
                self.item_translations,
                enabled_translations
            )

