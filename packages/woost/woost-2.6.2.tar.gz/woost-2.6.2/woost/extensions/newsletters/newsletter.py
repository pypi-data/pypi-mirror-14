#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import (
    Document,
    Slot,
    Template,
    Controller,
    CustomBlock,
    HTMLBlock,
    block_type_groups
)
from .newslettercontent import NewsletterContent
from .newsletterbox import NewsletterBox
from .newsletterlisting import NewsletterListing


class Newsletter(Document):

    default_template = schema.DynamicDefault(
        lambda: Template.get_instance(
            qname = "woost.extensions.newsletters.newsletter_template"
        )
    )

    default_controller = schema.DynamicDefault(
        lambda: Controller.get_instance(
            qname = "woost.extensions.newsletters.newsletter_controller"
        )
    )

    members_order = [
        "blocks"
    ]

    blocks = Slot()

    allowed_block_types = (
        NewsletterBox,
        NewsletterContent,
        NewsletterListing,
        CustomBlock,
        HTMLBlock
    )

    def allows_block_type(self, block_type):
        return issubclass(block_type, self.allowed_block_types)

