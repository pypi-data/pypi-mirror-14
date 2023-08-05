#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from PIL import Image
from cocktail.events import event_handler
from cocktail.iteration import first
from cocktail import schema
from woost.models.item import Item
from woost.models.rendering.renderer import Renderer

def _get_site_renderers():
    from woost.models import Configuration
    return Configuration.instance.renderers


class ImageFactory(Item):

    visible_from_root = False

    members_order = [
        "title",
        "identifier",
        "renderer",
        "default_format",
        "effects",
        "fallback",
        "applicable_to_blocks"
    ]

    title = schema.String(
        translated = True,
        descriptive = True
    )

    identifier = schema.String(
        unique = True,
        indexed = True,
        normalized_index = False
    )

    renderer = schema.Reference(
        required = True,
        type = Renderer,
        related_end = schema.Collection(),
        default = schema.DynamicDefault(
            lambda: first(_get_site_renderers())
        ),
        enumeration = lambda ctx: _get_site_renderers(),
        edit_control = "cocktail.html.DropdownSelector"
    )

    default_format = schema.String(
        enumeration = ["JPEG", "PNG", "GIF"],
        translatable_enumeration = False,
        edit_control = "cocktail.html.DropdownSelector"
    )

    effects = schema.Collection(
        items = "woost.models.rendering.ImageEffect",
        bidirectional = True,
        integral = True,
    )

    fallback = schema.Reference(
        type = "woost.models.rendering.ImageFactory",
        bidirectional = True
    )

    fallback_referers = schema.Collection(
        items = "woost.models.rendering.ImageFactory",
        bidirectional = True,
        visible = False,
        synchronizable = False
    )

    applicable_to_blocks = schema.Boolean(
        required = True,
        default = True,
        indexed = True
    )

    def render(self, item):

        image = self.renderer.render(item)

        if image is None:
            if self.fallback:
                image = self.fallback.render(item)
        else:
            if self.effects:
                if isinstance(image, basestring):
                    image = Image.open(image)

                for effect in self.effects:
                    image = effect.apply(image)

        return image

    cache_invalidators = frozenset((
        identifier,
        renderer,
        effects,
        fallback
    ))

    @event_handler
    def handle_changing(cls, e):
        from woost.models.rendering.request \
            import clear_image_cache_after_commit
        if e.source.is_inserted and e.member in cls.cache_invalidators:
            clear_image_cache_after_commit(factory = e.source)
            for referer in e.source.fallback_referers:
                clear_image_cache_after_commit(factory = referer)

    @event_handler
    def handle_related(cls, e):
        from woost.models.rendering.request \
            import clear_image_cache_after_commit
        if e.source.is_inserted and e.member in cls.cache_invalidators:
            clear_image_cache_after_commit(factory = e.source)
            for referer in e.source.fallback_referers:
                clear_image_cache_after_commit(factory = referer)

    @event_handler
    def handle_unrelated(cls, e):
        from woost.models.rendering.request \
            import clear_image_cache_after_commit
        if e.source.is_inserted and e.member in cls.cache_invalidators:
            clear_image_cache_after_commit(factory = e.source)
            for referer in e.source.fallback_referers:
                clear_image_cache_after_commit(factory = referer)

    @event_handler
    def handle_deleting(cls, e):
        from woost.models.rendering.request \
            import clear_image_cache_after_commit
        clear_image_cache_after_commit(factory = e.source)
        for referer in e.source.fallback_referers:
            clear_image_cache_after_commit(factory = referer)

