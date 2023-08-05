#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Website

Website.add_member(
    schema.String("google_analytics_account",
        text_search = False,
        member_group = "services.google_analytics",
        synchronizable = False,
        listed_by_default = False
    )
)

