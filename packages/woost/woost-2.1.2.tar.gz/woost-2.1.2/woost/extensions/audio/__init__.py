#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from woost.models import Extension, Configuration


translations.define("AudioExtension",
    ca = u"Àudio",
    es = u"Audio",
    en = u"Audio"
)

translations.define("AudioExtension-plural",
    ca = u"Àudio",
    es = u"Audio",
    en = u"Audio"
)


class AudioExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Reproducció de fitxers d'àudio amb recodificació automàtica a
            múltiples formats.""",
            "ca"
        )
        self.set("description",
            u"""Reproducción de ficheros de audio con recodificación automática
            a múltiples formatos.""",
            "es"
        )
        self.set("description",
            u"""Audio file player with transparent encoding in multiple
            formats.""",
            "en"
        )

    def _load(self):

        from woost.extensions.audio import (
            strings,
            configuration,
            audiodecoder,
            audioencoder
        )

        # Expose the controller for serving audio files in multiple encodings
        from woost.controllers.cmscontroller import CMSController
        from woost.extensions.audio.audioencodingcontroller \
            import AudioEncodingController

        CMSController.audio = AudioEncodingController

        self.install()
        self.register_view_factory()

    def _install(self):
        self.create_default_decoders()
        self.create_default_encoders()

    def create_default_decoders(self):

        from woost.extensions.audio.audiodecoder import AudioDecoder
        config = Configuration.instance

        mp3 = AudioDecoder()
        mp3.mime_type = "audio/mpeg"
        mp3.command = '/usr/bin/mpg321 "%s" -w -'
        mp3.insert()
        config.audio_decoders.append(mp3)

        ogg = AudioDecoder()
        ogg.mime_type = "audio/ogg"
        ogg.command = '/usr/bin/oggdec -Q -o - "%s"'
        ogg.insert()
        config.audio_decoders.append(ogg)

        flac = AudioDecoder()
        flac.mime_type = "audio/flac"
        flac.command = '/usr/bin/flac -dsc "%s"'
        flac.insert()
        config.audio_decoders.append(flac)

    def create_default_encoders(self):

        from woost.extensions.audio.audioencoder import AudioEncoder
        config = Configuration.instance

        mp3 = AudioEncoder()
        mp3.identifier = "mp3-128"
        mp3.mime_type = "audio/mpeg"
        mp3.extension = ".mp3"
        mp3.command = "/usr/bin/lame --quiet -b 128 - %s"
        mp3.insert()
        config.audio_encoders.append(mp3)

        ogg = AudioEncoder()
        ogg.identifier = "ogg-q5"
        ogg.mime_type = "audio/ogg"
        ogg.extension = ".ogg"
        ogg.command = "/usr/bin/oggenc -q 5 - -o %s"
        ogg.insert()
        config.audio_encoders.append(ogg)

    def register_view_factory(self):

        from woost.models import Publishable
        from woost.extensions.audio.audioplayer import AudioPlayer
        from woost.views.viewfactory import publishable_view_factory

        def audio_player(item, parameters):
            if item.resource_type == "audio":
                player = AudioPlayer()
                player.file = item
                return player

        publishable_view_factory.register_first(Publishable, "audio_player", audio_player)

