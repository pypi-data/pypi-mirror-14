#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import LocaleMember
from woost.views.uigeneration import backoffice_edit_control


class TranslationWorkflowPath(schema.Tuple):

    def __init__(self, *args, **kwargs):
        kwargs["items"] = (
            LocaleMember("source_language",
                required = True,
            ),
            LocaleMember("target_language",
                required = True
            )
        )
        kwargs["request_value_separator"] = ":"
        schema.Tuple.__init__(self, *args, **kwargs)

    def translate_value(self, value, language = None, **kwargs):
        if value:
            try:
                return translations(
                    "woost.extensions.translationworkflow.translation_path",
                    source_language = value[0],
                    target_language = value[1],
                    language = language,
                    **kwargs
                )
            except Exception, error:
                pass

        return schema.Tuple.translate_value(
            self,
            value,
            language = language,
            **kwargs
        )


backoffice_edit_control.set_member_type_display(
    TranslationWorkflowPath,
    "woost.extensions.translationworkflow.TranslationWorkflowPathEditor"
)

