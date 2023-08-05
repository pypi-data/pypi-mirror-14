#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from cocktail.html import templates
from cocktail.typemapping import TypeMapping
from woost.models.item import Item
from woost.models.file import File


class VideoPlayerSettings(Item):

    instantiable = True
    visible_from_root = False
    player_initialization = TypeMapping()

    members_order = [
        "title", "width", "height", "autoplay", "show_player_controls"
    ]

    title = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        spellcheck = True
    )

    width = schema.Integer(
        required = True,
        default = 480,
        listed_by_default = False
    )

    height = schema.Integer(
        required = True,
        default = 385,
        listed_by_default = False
    )

    autoplay = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False
    )

    show_player_controls = schema.Boolean(
        required = True,
        default = True,
        listed_by_default = False
    )

    def create_player(self, video):
        player = templates.new(video.video_player)
        player_initialization = self.player_initialization.get(video.__class__)
        if player_initialization:
            player_initialization(player, self, video)
        return player


def player_initialization(player, settings, video):
    player.width = settings.width
    player.height = settings.height
    player.autoplay = settings.autoplay
    player.show_player_controls = settings.show_player_controls
    player.sources = ((video.get_uri(), video.mime_type),)

VideoPlayerSettings.player_initialization[File] = player_initialization

