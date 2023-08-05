#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Configuration, Document

Configuration.members_order.extend([
    "google_search_engine_id",
    "google_search_results_page"
])

Configuration.add_member(
    schema.String("google_search_engine_id",
        member_group = "services.google_cse",
        listed_by_default = False
    )
)

Configuration.add_member(
    schema.Reference("google_search_results_page",
        type = Document,
        related_end = schema.Collection(),
        member_group = "services.google_cse",
        listed_by_default = False
    )
)

