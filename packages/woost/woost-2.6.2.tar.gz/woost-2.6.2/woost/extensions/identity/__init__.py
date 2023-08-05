#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension


translations.define("IdentityExtension",
    ca = u"Identitat",
    es = u"Identidad",
    en = u"Identity"
)

translations.define("IdentityExtension-plural",
    ca = u"Identitat",
    es = u"Identidad",
    en = u"Identity"
)


class IdentityExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""
                Integració de serveis d'autenticació externs (Facebook,
                Google, etc).
            """,
            "ca"
        )
        self.set("description",
            u"""
                Integración de servicios de autenticación externos (Facebook,
                Google, etc).
                """,
            "es"
        )
        self.set("description",
            u"""
                Integration with external authentication providers (Facebook,
                Google, etc).
            """,
            "en"
        )

    def _load(self):

        from woost.extensions.identity import (
            strings,
            configuration,
            identityprovider,
            facebook,
            google
        )

        templates.get_class("woost.extensions.identity.LoginBlockViewOverlay")
        templates.get_class("woost.extensions.identity.ItemCardOverlay")

