#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension


translations.define("NoticesExtension",
    ca = u"Avisos",
    es = u"Avisos",
    en = u"Notices"
)

translations.define("NoticesExtension-plural",
    ca = u"Avisos",
    es = u"Avisos",
    en = u"Notices"
)


class NoticesExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet mostrar avisos als visitants de la web.""",
            "ca"
        )
        self.set("description",
            u"""Permite mostrar avisos als visitants de la web.""",
            "es"
        )
        self.set("description",
            u"""Show notices to website visitors.""",
            "en"
        )

    def _load(self):

        from woost.extensions.notices import (
            strings,
            website
        )

