#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import File, VideoPlayerSettings
from woost.extensions.vimeo.vimeovideo import VimeoVideo


VideoPlayerSettings.members_order = VideoPlayerSettings.members_order + [
        "vimeo_loop",
        "vimeo_allow_fullscreen",
        "vimeo_title",
        "vimeo_byline",
        "vimeo_portrait",
        "vimeo_color"
]

VideoPlayerSettings.add_member(
    schema.Boolean(
        "vimeo_loop",
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "vimeo"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "vimeo_allow_fullscreen",
        default = True,
        listed_by_default = False,
        member_group = "vimeo"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "vimeo_title",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "vimeo"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "vimeo_byline",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "vimeo"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "vimeo_portrait",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "vimeo"
    )
)

VideoPlayerSettings.add_member(
    schema.Color(
        "vimeo_color",
        listed_by_default = False,
        member_group = "vimeo"
    )
)

def player_initialization(player, settings, video):
    player.video_id = video.video_id
    player.width = settings.width
    player.height = settings.height
    player.vimeo_autoplay = settings.autoplay
    player.allow_fullscreen = settings.vimeo_allow_fullscreen
    player.vimeo_loop = settings.vimeo_loop
    player.vimeo_title = settings.vimeo_title
    player.vimeo_byline = settings.vimeo_byline
    player.vimeo_portrait = settings.vimeo_portrait
    player.vimeo_color = settings.vimeo_color

VideoPlayerSettings.player_initialization[VimeoVideo] = player_initialization

