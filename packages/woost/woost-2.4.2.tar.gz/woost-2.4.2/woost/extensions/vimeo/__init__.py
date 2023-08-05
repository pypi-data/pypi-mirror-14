#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations
from woost.models import Extension, Configuration, VideoPlayerSettings
from woost.models.rendering import ChainRenderer


translations.define("VimeoExtension",
    ca = u"Vimeo",
    es = u"Vimeo",
    en = u"Vimeo"
)

translations.define("VimeoExtension-plural",
    ca = u"Vimeo",
    es = u"Vimeo",
    en = u"Vimeo"
)


class VimeoExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Afegeix suport per vídeos de Vimeo""",
            "ca"
        )
        self.set("description",
            u"""Añade soporte para videos de Vimeo""",
            "es"
        )
        self.set("description",
            u"""Adds support for Vimeo videos""",
            "en"
        )

    def _load(self):
        from woost.extensions.vimeo import (
            strings,
            vimeovideo,
            videoplayersettings
        )

        self.install()

    def _install(self):
        self._create_renderers()

    def _create_renderers(self):

        from woost.extensions.vimeo.vimeovideorenderer \
            import VimeoVideoRenderer

        # Look for the first chain renderer
        for renderer in Configuration.instance.renderers:
            if isinstance(renderer, ChainRenderer):

                # Add the renderer for Vimeo videos
                vimeo_renderer = VimeoVideoRenderer()
                vimeo_renderer.insert()
                renderer.renderers.append(vimeo_renderer)

                break

