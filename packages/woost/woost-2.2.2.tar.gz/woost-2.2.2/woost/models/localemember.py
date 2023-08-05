#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.stringutils import normalize
from cocktail.translations import translations
from cocktail import schema


class LocaleMember(schema.String):

    def __init__(self, *args, **kwargs):
        from woost.models.configuration import Configuration
        kwargs.setdefault("search_control", "cocktail.html.DropdownSelector")
        kwargs.setdefault(
            "enumeration",
            lambda ctx: sorted(
                Configuration.instance.languages,
                key = lambda locale: normalize(self.translate_value(locale))
            )
        )
        schema.String.__init__(self, *args, **kwargs)

    def translate_value(self, value, language = None, **kwargs):
        if not value:
            return schema.String.translate_value(
                self,
                value,
                language = language,
                **kwargs
            )
        else:
            return translations(
                "locale",
                locale = value,
                language = language,
                **kwargs
            )

