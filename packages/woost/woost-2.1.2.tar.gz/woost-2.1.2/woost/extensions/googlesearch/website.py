#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Website, Document


Website.add_member(
    schema.String("google_search_engine_id",
        member_group = "services.google_cse"
    )
)

Website.add_member(
    schema.Reference("google_search_results_page",
        type = Document,
        related_end = schema.Collection(),
        member_group = "services.google_cse"
    )
)

