#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Block, Slot


class NewsletterBox(Block):

    type_group = "blocks.newsletter"

    members_order = [
        "view_class",
        "blocks"
    ]

    view_class = schema.String(
        shadows_attribute = True,
        required = True,
        default = "woost.extensions.newsletters.NewsletterBoxView",
        enumeration = [
            "woost.extensions.newsletters.NewsletterBoxView"
        ],
        text_search = False,
        member_group = "content"
    )

    blocks = Slot()

