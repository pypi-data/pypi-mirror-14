#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Publishable
from .block import Block


class TweetButton(Block):

    instantiable = True
    type_group = "blocks.social"
    view_class = "woost.views.TweetButton"

    groups_order = list(Block.groups_order)
    pos = groups_order.index("content")
    groups_order = (
        groups_order[:pos + 1]
        + ["tweet", "appearence"]
        + groups_order[pos + 1:]
    )
    del pos

    members_order = [
        "tw_target",
        "tw_via",
        "tw_related",
        "tw_hashtags",
        "tw_text",
        "tw_dnt",
        "tw_size",
        "tw_count"
    ]

    tw_target = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "tweet"
    )

    tw_via = schema.String(
        member_group = "tweet"
    )

    tw_related = schema.String(
        member_group = "tweet"
    )

    tw_hashtags = schema.String(
        member_group = "tweet"
    )

    tw_text = schema.String(
        translated = True,
        edit_control = "cocktail.html.TextArea",
        member_group = "tweet"
    )

    tw_dnt = schema.Boolean(
        required = True,
        default = False,
        member_group = "tweet"
    )

    tw_size = schema.String(
        required = True,
        default = "medium",
        enumeration = ["medium", "big"],
        edit_control = "cocktail.html.RadioSelector",
        member_group = "appearence"
    )

    tw_count = schema.String(
        required = True,
        default = "horizontal",
        enumeration = ["none", "horizontal", "vertical"],
        edit_control = "cocktail.html.RadioSelector",
        member_group = "appearence"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.url = self.tw_target and self.tw_target.get_uri(host = ".")
        view.via = self.tw_via
        view.related = self.tw_related
        view.hashtags = self.tw_hashtags
        view.dnt = self.tw_dnt
        view.text = self.tw_text
        view.size = self.tw_size
        view.count = self.tw_count

