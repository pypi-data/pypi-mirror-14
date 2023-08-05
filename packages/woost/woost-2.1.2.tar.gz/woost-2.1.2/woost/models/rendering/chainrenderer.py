#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models.rendering.renderer import Renderer


class ChainRenderer(Renderer):

    instantiable = True

    renderers = schema.Collection(
        items = schema.Reference(type = Renderer),
        bidirectional = True,
        integral = True,
        related_end = schema.Reference()
    )

    def can_render(self, item):
        return any(renderer.can_render(item) for renderer in self.renderers)

    def render(self, item, **parameters):
        for renderer in self.renderers:
            if renderer.can_render(item, **parameters):
                return renderer.render(item, **parameters)


