#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.events import when
from cocktail import schema
from cocktail.controllers import request_property
from woost.models import Publishable, VideoPlayerSettings
from .block import Block
from .elementtype import ElementType


class VideoBlock(Block):

    instantiable = True
    block_display = "woost.views.VideoBlockDisplay"

    member_order = ["element_type", "video", "player_settings"]

    element_type = ElementType(
        member_group = "content"
    )

    video = schema.Reference(
        type = Publishable,
        required = True,
        relation_constraints = {"resource_type": "video"},
        related_end = schema.Collection(),
        invalidates_cache = True,
        member_group = "content"
    )

    player_settings = schema.Reference(
        type = VideoPlayerSettings,
        required = True,
        related_end = schema.Collection(),
        invalidates_cache = True,
        member_group = "content"
    )

    view_class = schema.String(
        required = True,
        shadows_attribute = True,
        enumeration = [
            "woost.views.VideoBlockView",
            "woost.views.VideoPopUp"
        ],
        default = "woost.views.VideoBlockView",
        edit_control = "cocktail.html.RadioSelector",
        member_group = "content"
    )


    def get_block_image(self):
        return self.video

    def init_view(self, view):
        Block.init_view(self, view)
        view.tag = self.element_type
        view.video = self.video
        view.player_settings = self.player_settings
        view.depends_on(self.video)

