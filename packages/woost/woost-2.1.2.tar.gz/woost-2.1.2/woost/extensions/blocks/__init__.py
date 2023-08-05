#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from warnings import warn
from cocktail.translations import translations
from woost.models import Extension


translations.define("BlocksExtension",
    ca = u"Blocs de contingut",
    es = u"Bloques de contenido",
    en = u"Content blocks"
)

translations.define("BlocksExtension-plural",
    ca = u"Blocs de contingut",
    es = u"Bloques de contenido",
    en = u"Content blocks"
)


class BlocksExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet la creació de contingut utilitzant blocs""",
            "ca"
        )
        self.set("description",
            u"""Permite la creación de contenido usando bloques""",
            "es"
        )
        self.set("description",
            u"""Allows the creation of content using blocs""",
            "en"
        )

    def _load(self):
        warn(
            "The blocks extension has been integrated with the core and is "
            "no longer necessary",
            DeprecationWarning
        )

