#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.pkgutils import resolve
from cocktail.events import event_handler
from cocktail import schema
from woost import app
from woost.models.rendering.renderer import Renderer


class IconRenderer(Renderer):

    instantiable = True

    members_order = [
        "icon_size",
        "icon_resolver_expression"
    ]

    icon_size = schema.Integer(
        required = True,
        enumeration = [16, 32],
        edit_control = "cocktail.html.RadioSelector"
    )

    icon_resolver_expression = schema.String()

    def can_render(self, item, **parameters):
        return True

    def render(self, item, **parameters):
        return self.icon_resolver.find_icon_path(item, self.icon_size)

    @property
    def icon_resolver(self):
        try:
            return self._v_icon_resolver
        except AttributeError:
            expr = self.icon_resolver_expression
            icon_resolver = resolve(expr) if expr else app.icon_resolver
            self._v_icon_resolver = icon_resolver
            return icon_resolver

    @event_handler
    def handle_changed(cls, e):
        if e.member is cls.icon_resolver_expression:
            e.source._v_icon_resolver = None

