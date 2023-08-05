#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema


class ElementType(schema.String):

    required = True
    default = "div"
    enumeration = [
        "div",
        "section",
        "article",
        "details",
        "aside",
        "figure",
        "header",
        "footer",
        "nav",
        "dd"
    ]

    def translate_value(self, value, language = None, **kwargs):

        translation = schema.String.translate_value(
            self,
            value,
            language,
            **kwargs
        )

        if (
            not translation
            and value
            and self.translatable_enumeration
            and self.enumeration
        ):
            translation = translations("woost.models.ElementType=" + value)

        return translation

