#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations
from woost.models import Extension, Configuration
from woost.models.rendering import ChainRenderer


translations.define("YouTubeExtension",
    ca = u"YouTube",
    es = u"YouTube",
    en = u"YouTube"
)

translations.define("YouTubeExtension-plural",
    ca = u"YouTube",
    es = u"YouTube",
    en = u"YouTube"
)


class YouTubeExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Afegeix suport per vídeos de YouTube""",
            "ca"
        )
        self.set("description",
            u"""Añade soporte para videos de YouTube""",
            "es"
        )
        self.set("description",
            u"""Adds support for YouTube videos""",
            "en"
        )

    def _load(self):
        from woost.extensions.youtube import (
            strings,
            youtubevideo,
            videoplayersettings
        )

        self.install()

    def _install(self):
        self._create_renderers()

    def _create_renderers(self):

        from woost.extensions.youtube.youtubevideorenderer \
            import YouTubeVideoRenderer

        # Look for the first chain renderer
        for renderer in Configuration.instance.renderers:
            if isinstance(renderer, ChainRenderer):

                # Add the renderer for YouTube videos
                youtube_renderer = YouTubeVideoRenderer()
                youtube_renderer.insert()
                renderer.renderers.append(youtube_renderer)

                break

