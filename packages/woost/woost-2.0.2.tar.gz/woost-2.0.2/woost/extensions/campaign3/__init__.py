#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import Extension, Controller, Configuration
from woost.models.rendering import ChainRenderer


translations.define("CampaignMonitor3Extension",
    ca = u"Campaign Monitor v3",
    es = u"Campaign Monitor v3",
    en = u"Campaign Monitor v3"
)

translations.define("CampaignMonitor3Extension-plural",
    ca = u"Campaign Monitor v3",
    es = u"Campaign Monitor v3",
    en = u"Campaign Monitor v3"
)


class CampaignMonitor3Extension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet la integració amb el sistema de mailing Campaign Monitor""",
            "ca"
        )
        self.set("description",
            u"""Permite la integración con el sistema de mailing Campaign Monitor""",
            "es"
        )
        self.set("description",
            u"""Allows the integration with the Campaign Monitor mailing system""",
            "en"
        )

    def _load(self):

        from woost.extensions.campaign3 import (
            strings,
            configuration,
            website,
            campaignmonitorlist,
            subscriptionformblock
        )

    def _install(self):
        pass

