#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Block, Publishable


class NewsletterListing(Block):

    type_group = "blocks.newsletter"

    members_order = [
        "view_class",
        "listed_items"
    ]

    view_class = schema.String(
        shadows_attribute = True,
        default = "woost.extensions.newsletters.NewsletterListingTextOnlyView",
        enumeration = [
            "woost.extensions.newsletters.NewsletterListingTextOnlyView",
            "woost.extensions.newsletters.NewsletterListingTextAndIconView",
            "woost.extensions.newsletters.NewsletterListingSummaryView"
        ],
        required = True,
        text_search = False,
        member_group = "content"
    )

    listed_items = schema.Collection(
        items = schema.Reference(type = Publishable),
        related_end = schema.Collection(),
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.listed_items = self.listed_items

