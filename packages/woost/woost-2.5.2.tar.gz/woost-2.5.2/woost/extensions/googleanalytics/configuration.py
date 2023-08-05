#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Configuration

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
    schema.String("google_analytics_api",
        required = True,
        enumeration = ["ga.js", "universal"],
        translatable_enumeration = False,
        default = "ga.js",
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

