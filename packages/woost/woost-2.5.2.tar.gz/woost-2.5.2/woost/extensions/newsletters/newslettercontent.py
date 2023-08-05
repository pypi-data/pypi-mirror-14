#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.iteration import first
from cocktail import schema
from woost.models import Block, Publishable, File
from woost.models.rendering import ImageFactory


class NewsletterContent(Block):

    type_group = "blocks.newsletter"

    members_order = [
        "view_class",
        "text",
        "image",
        "image_alignment",
        "image_factory",
        "link"
    ]

    view_class = schema.String(
        shadows_attribute = True,
        required = True,
        default = "woost.extensions.newsletters.NewsletterContentView",
        enumeration = [
            "woost.extensions.newsletters.NewsletterContentView"
        ],
        text_search = False,
        member_group = "content"
    )

    text = schema.HTML(
        edit_control = "woost.extensions.newsletters.NewsletterRichTextEditor",
        translated = True,
        member_group = "content"
    )

    image = schema.Reference(
        type = File,
        related_end = schema.Collection(),
        member_group = "content"
    )

    image_alignment = schema.String(
        required = True,
        enumeration = [
            "image_left",
            "image_right",
            "image_top"
        ],
        text_search = False,
        member_group = "content"
    )

    image_factory = schema.Reference(
        type = ImageFactory,
        related_end = schema.Collection(),
        relation_constraints = {
            "applicable_to_newsletters": True
        },
        edit_control = "cocktail.html.DropdownSelector",
        member_group = "content"
    )

    link = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.text = self.text
        view.image = self.image
        view.image_alignment = self.image_alignment
        view.image_factory = self.image_factory
        view.link = self.link

