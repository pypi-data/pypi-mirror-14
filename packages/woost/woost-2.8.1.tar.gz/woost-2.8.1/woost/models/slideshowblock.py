#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.html import templates
from .rendering import ImageFactory
from .block import Block
from .slot import Slot
from .elementtype import ElementType
from .blockutils import create_block_views


class SlideShowBlock(Block):

    instantiable = True
    view_class = "woost.views.SlideShowBlockView"

    groups_order = [
        "content",
        "transition_settings",
        "controls",
        "behavior",
        "html",
        "administration"
    ]

    members_order = [
        "element_type",
        "slides",
        "autoplay",
        "interval",
        "transition_effect",
        "transition_duration",
        "navigation_controls",
        "bullet_controls",
        "bullet_view_class",
        "bullet_image_factory"
    ]

    element_type = ElementType(
        enumeration = list(ElementType.enumeration),
        member_group = "content"
    )

    for et in ("nav", "dd"):
        try:
            element_type.enumeration.remove(et)
        except:
            pass

    slides = Slot()

    autoplay = schema.Boolean(
        required = True,
        default = True,
        member_group = "transition_settings"
    )

    interval = schema.Integer(
        required = autoplay,
        default = 3000,
        min = 0,
        member_group = "transition_settings"
    )

    transition_effect = schema.String(
        required = True,
        default = "fade",
        enumeration = ["fade", "topBottomSlide"],
        member_group = "transition_settings"
    )

    transition_duration = schema.Integer(
        required = True,
        default = 500,
        min = 0,
        member_group = "transition_settings"
    )

    navigation_controls = schema.Boolean(
        required = True,
        default = False,
        member_group = "controls"
    )

    bullet_controls = schema.Boolean(
        required = True,
        default = False,
        member_group = "controls"
    )

    bullet_view_class = schema.String(
        required = True,
        default = "woost.views.SlideShowButtonBullet",
        enumeration = [
            "woost.views.SlideShowButtonBullet",
            "woost.views.SlideShowTextBullet",
            "woost.views.SlideShowImageBullet",
            "woost.views.SlideShowTextAndImageBullet"
        ],
        member_group = "controls"
    )

    bullet_image_factory = schema.Reference(
        type = ImageFactory,
        related_end = schema.Collection(),
        required = True,
        default = schema.DynamicDefault(
            lambda: ImageFactory.get_instance(identifier = "image_gallery_thumbnail")
        ),
        member_group = "controls"
    )

    def init_view(self, view):

        Block.init_view(self, view)

        view.tag = self.element_type
        view.autoplay = self.autoplay
        view.interval = self.interval
        view.transition_effect = self.transition_effect
        view.transition_duration = self.transition_duration
        view.navigation_controls = self.navigation_controls
        view.bullet_controls = self.bullet_controls
        view.bullet_view_class = self.bullet_view_class
        view.bullet_image_factory = self.bullet_image_factory

        for block_view in create_block_views(self.slides):
            view.slides.append(block_view)

