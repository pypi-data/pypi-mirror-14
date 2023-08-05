#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension


translations.define("AnnotationsExtension",
    ca = u"Annotacions",
    es = u"Anotaciones",
    en = u"Annotations"
)

translations.define("AnnotationsExtension-plural",
    ca = u"Annotacions",
    es = u"Anotaciones",
    en = u"Annotations"
)


class AnnotationsExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet afegir annotacions als camps durant l'edició.""",
            "ca"
        )
        self.set("description",
            u"""Permite añadir anotaciones a los campos durante la edición.""",
            "es"
        )
        self.set("description",
            u"""Annotate editable fields.""",
            "en"
        )

    def _load(self):

        from woost.extensions.annotations import (
            strings,
            annotations
        )

        templates.get_class("woost.extensions.annotations.BackOfficeFieldsViewOverlay")

