#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block


class TwitterTimelineBlock(Block):

    instantiable = True
    type_group = "blocks.social"
    view_class = "cocktail.html.TwitterTimeline"

    members_order = [
        "widget_id",
        "theme",
        "link_color",
        "width",
        "height",
        "related_accounts"
    ]

    widget_id = schema.String(
        required = True,
        member_group = "content"
    )

    theme = schema.String(
        required = True,
        default = "light",
        enumeration = ("light", "dark"),
        member_group = "appearence"
    )

    link_color = schema.Color(
        member_group = "appearence"
    )

    width = schema.Integer(
        member_group = "appearence"
    )

    height = schema.Integer(
        member_group = "appearence"
    )

    related_accounts = schema.String(
        member_group = "tweet"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.widget_id = self.widget_id
        view.theme = self.theme
        view.link_color = self.link_color
        view.width = self.width
        view.height = self.height
        view.related = self.related_accounts

