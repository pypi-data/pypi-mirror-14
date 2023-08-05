#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Document

Document.add_member(
    schema.Boolean("ga_tracking_enabled",
        default = True,
        required = True,
        listed_by_default = False,
        member_group = "meta"
    )
)

Document.is_ga_tracking_enabled = lambda self: self.ga_tracking_enabled
