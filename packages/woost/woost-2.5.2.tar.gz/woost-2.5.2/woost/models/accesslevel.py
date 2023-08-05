#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import Item


class AccessLevel(Item):

    type_group = "users"

    members_order = [
        "title",
        "roles_with_access",
        "restricted_content"
    ]

    title = schema.String(
        translated = True,
        unique = True,
        indexed = True,
        normalized_index = False
    )

    roles_with_access = schema.Collection(
        items = "woost.models.Role",
        bidirectional = True
    )

    restricted_content = schema.Collection(
        items = "woost.models.Publishable",
        bidirectional = True,
        editable = False
    )

    def __translate__(self, language, **kwargs):

        if self.title:
            return self.title

        if self.roles_with_access:
            return translations(
                "woost.models.accesslevel.AccessLevel-instance",
                instance = self
            )

        return Item.__translate__(self, language, **kwargs)

