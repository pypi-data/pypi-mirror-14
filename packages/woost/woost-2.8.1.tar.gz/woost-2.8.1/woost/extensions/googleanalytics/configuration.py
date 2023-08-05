#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Configuration, LocaleMember
from .customdefinition import GoogleAnalyticsCustomDefinition

Configuration.add_member(
    schema.String("google_analytics_account",
        text_search = False,
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

Configuration.add_member(
    schema.String("google_analytics_domain",
        text_search = False,
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

Configuration.add_member(
    LocaleMember("google_analytics_language",
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

Configuration.add_member(
    schema.Collection("google_analytics_custom_definitions",
        items = schema.Reference(type = GoogleAnalyticsCustomDefinition),
        related_end = schema.Reference(),
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

