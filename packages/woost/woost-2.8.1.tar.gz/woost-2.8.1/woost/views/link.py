#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import Element
from woost.models import get_current_user, ReadPermission


class Link(Element):

    NO_CHECK = 0
    REQUIRE_PUBLISHED = 1
    REQUIRE_READABLE = 2
    REQUIRE_ACCESSIBLE = REQUIRE_PUBLISHED | REQUIRE_READABLE

    NO_EFFECT = 0
    HIDE = 1
    BECOME_TRANSPARENT = 2
    BECOME_SPAN = 3

    tag = "a"
    value = None
    language = None
    host = None
    parameters = None
    path = None
    content_check = REQUIRE_ACCESSIBLE
    inactive_behavior = HIDE

    def _ready(self):

        active = (
            self.value is not None
            and not (
                self.content_check & self.REQUIRE_PUBLISHED
                and not self.value.is_published(self.language)
            )
            and not (
                self.content_check & self.REQUIRE_READABLE
                and not get_current_user().has_permission(
                    ReadPermission,
                    target = self.value
                )
            )
        )

        if not active:
            self._deactivate_link()

        Element._ready(self)

        if active:
            uri = self.get_uri()
            if uri:
                self["href"] = uri
            else:
                self._deactivate_link()

    def _deactivate_link(self):
        if self.inactive_behavior == self.HIDE:
            self.visible = False
        elif self.inactive_behavior == self.BECOME_TRANSPARENT:
            self.tag = None
        elif self.inactive_behavior == self.BECOME_SPAN:
            self.tag = "span"
        elif self.inactive_behavior != self.NO_EFFECT:
            raise ValueError(
                "Unsupported value for Link.inactive_behavior (%r)"
                % self.inactive_behavior
            )

    def get_uri(self):
        if not self.value:
            return None
        else:
            return self.value.get_uri(
                language = self.language,
                host = self.host,
                path = self.path,
                parameters = self.parameters
            )

