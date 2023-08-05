#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from woost.models import Extension, Role, ReadPermission

translations.define("RestrictedAccessExtension",
    ca = u"Restricció d'accés",
    es = u"Restricción de acceso",
    en = u"Access restriction"
)

translations.define("RestrictedAccessExtension-plural",
    ca = u"Restricció d'accés",
    es = u"Restricción de acceso",
    en = u"Access restriction"
)


class RestrictedAccessExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"Facilita la definició de diferents conjunts d'elements "
            u"publicables amb accés restringit.",
            "ca"
        )
        self.set("description",
            u"Facilita la definición de diferentes conjuntos de elementos "
            u"publicables con acceso restringido.",
            "es"
        )
        self.set("description",
            u"Simplifies the definition of different sets of publishable "
            u"elements with restricted access.",
            "en"
        )

    def _load(self):

        from woost.extensions.restrictedaccess import (
            strings,
            publishable,
            accessrestriction
        )

    def _install(self):
        self.setup_permissions()

    def setup_permissions(self):

        everybody_role = Role.require_instance(qname = "woost.everybody")

        qname = "woost.extensions.restrictedaccess.restriction"
        restriction = ReadPermission.get_instance(qname = qname)

        if restriction is None:
            restriction = ReadPermission()
            restriction.qname = qname
            restriction.authorized = False

        restriction.matching_items = {
            "type": "woost.models.publishable.Publishable",
            "filter": "member-access_restriction",
            "filter_operator0": "ne",
            "filter_value0": ""
        }
        restriction.insert()

        if restriction not in everybody_role.permissions:
            everybody_role.permissions.insert(0, restriction)

