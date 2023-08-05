#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import when
from cocktail.translations import iter_derived_languages
from cocktail import schema

def auto_enables_translations(cls):

    @when(cls.adding_translation)
    def handle_adding_translation(event):
        auto_enable_translations(
            event.language,
            event.source.translations,
            event.source.enabled_translations
        )

    @when(cls.removing_translation)
    def handle_removing_translation(event):
        auto_disable_translations(
            event.language,
            event.source.translations,
            event.source.enabled_translations
        )

    return cls

def auto_enable_translations(
    language,
    defined_translations,
    enabled_translations
):
    from woost.models import Configuration
    if language not in Configuration.instance.virtual_languages:
        schema.add(enabled_translations, language)

    for derived_language in iter_derived_languages(language):
        if derived_language not in defined_translations:
            auto_enable_translations(
                derived_language,
                defined_translations,
                enabled_translations
            )

def auto_disable_translations(
    language,
    defined_translations,
    enabled_translations
):
    try:
        schema.remove(enabled_translations, language)
    except (ValueError, KeyError):
        pass

    for derived_language in iter_derived_languages(language):
        if derived_language not in defined_translations:
            auto_disable_translations(
                derived_language,
                defined_translations,
                enabled_translations
            )

