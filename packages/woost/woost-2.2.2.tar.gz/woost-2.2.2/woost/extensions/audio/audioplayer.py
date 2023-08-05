#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.html import Element
from mimetypes import guess_type
from woost.extensions.audio.request import get_audio_uri


class AudioPlayer(Element):

    tag = "audio"
    file = None
    encodings = [".ogg", ".mp3"]
    media_element_defaults = {}

    def _build(self):
        self["controls"] = "controls"
        self["preload"] = "auto"
        self.media_element_options = self.media_element_defaults.copy()
        self.add_resource("/cocktail/mediaelement/mediaelementplayer.min.css")
        self.add_resource("/cocktail/mediaelement/mediaelement-and-player.min.js")
        self.add_client_code("jQuery(this).mediaelementplayer(this.mediaElementOptions);")

    def _ready(self):

        self.set_client_param(
            "mediaElementOptions",
            self.media_element_options
        )

        for encoding in self.encodings:
            url = get_audio_uri(self.file, encoding)
            if url:
                source = Element("source")
                source["src"] = url

                mime_type = guess_type(url, strict = False)
                if mime_type:
                    source["type"] = mime_type[0]

                self.append(source)

        Element._ready(self)

