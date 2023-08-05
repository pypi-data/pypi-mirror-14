#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.stringutils import normalize
from cocktail.translations import translations
from cocktail.html import templates

List = templates.get_class("cocktail.html.List")


class TranslationsList(List):

    def _fill_entries(self):
        self.items = list(self.items)
        self.items.sort(
            key = lambda locale:
                normalize(translations("locale", locale = locale))
        )
        List._fill_entries(self)

    def create_entry_content(self, item):
        return translations("locale", locale = item)

