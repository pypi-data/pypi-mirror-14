#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import VideoPlayerSettings
from woost.extensions.tv3alacarta.tv3alacartavideo import TV3ALaCartaVideo

def player_initialization(player, settings, video):
    player.video = video
    player.width = settings.width
    player.height = settings.height
    player.autoplay = settings.autoplay
    player.show_player_controls = settings.show_player_controls

VideoPlayerSettings.player_initialization[TV3ALaCartaVideo] = player_initialization

