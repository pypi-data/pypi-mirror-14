#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import VideoPlayerSettings
from woost.extensions.youtube.youtubevideo import YouTubeVideo


VideoPlayerSettings.members_order = VideoPlayerSettings.members_order + [
        "youtube_allow_fullscreen",
        "youtube_show_info",
        "youtube_show_related_videos"
    ]

VideoPlayerSettings.add_member(
    schema.Boolean(
        "youtube_allow_fullscreen",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "youtube"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "youtube_show_info",
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "youtube"
    )
)

VideoPlayerSettings.add_member(
    schema.Boolean(
        "youtube_show_related_videos",
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "youtube"
    )
)


def player_initialization(player, settings, video):
    player.video_id = video.video_id
    player.width = settings.width
    player.height = settings.height
    player.autoplay = settings.autoplay
    player.show_player_controls = settings.show_player_controls
    player.allow_fullscreen = settings.youtube_allow_fullscreen
    player.show_info = settings.youtube_show_info
    player.show_related_videos = settings.youtube_show_related_videos

VideoPlayerSettings.player_initialization[YouTubeVideo] = player_initialization

