#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2008
"""
from cocktail import schema
from cocktail.html import Element
from cocktail.translations import translations
from cocktail.controllers import context
from woost import app
from woost.models.rendering import Renderer
from woost.models.utils import any_translation


class ItemLabel(Element):

    item = None
    image_factory = "backoffice_small_thumbnail.png"
    icon_visible = "auto"
    label_visible = True
    referer = None
    language_chain = None

    # Make the view usable as a member display
    def _get_value(self):
        return self.item

    def _set_value(self, value):
        self.item = value

    value = property(_get_value, _set_value)

    def should_display_icon(self):

        if self.icon_visible == "auto":

            # Models can request that their icons be always visible
            if self.item.icon_conveys_information:
                return True

            # Distinguish types
            if self.member:

                if isinstance(self.member, schema.Reference):
                    related_type = self.member.related_type
                elif isinstance(self.member, schema.Schema):
                    related_type = self.member
                else:
                    related_type = None

                if related_type is not None:
                    icons = set()

                    for cls in related_type.schema_tree():
                        if cls.icon_conveys_information:
                            return True
                        if cls.visible and cls.instantiable:
                            icons.add(app.icon_resolver.find_icon(cls, 16))
                            if len(icons) > 1:
                                return True

            # Images
            renderer = Renderer.get_instance(qname = "woost.content_renderer")
            if renderer is not None:
                if renderer.can_render(self.item):
                    return True

                image = self.item.get_representative_image()
                if image is not None and renderer.can_render(image):
                    return True

            return False

        return self.icon_visible

    def _ready(self):
        Element._ready(self)

        if self.item:
            self["draggable"] = "true"
            self["data-woost-item"] = self.item.id

            for schema in self.item.__class__.descend_inheritance(True):
                self.add_class(schema.name)

            if self.should_display_icon():
                self.add_class("with_icon")
                self.append(self.create_icon())

            if self.label_visible:
                self.text_wrapper = self.create_text_wrapper()
                self.append(self.text_wrapper)

    def create_icon(self):
        img = Element("img")
        img.add_class("icon")
        img["title"] = translations(self.item.__class__.__name__)
        get_image_uri = getattr(self.item, "get_image_uri", None)

        if get_image_uri:
            img["src"] = get_image_uri(self.image_factory)
        else:
            image_factory = self.image_factory or "default"

            if "." not in image_factory:
                from woost.models.rendering.formats import (
                    extensions_by_format,
                    default_format
                )
                extension = extensions_by_format[default_format]
                image_factory += "." + extension

            img["src"] = context["cms"].image_uri(self.item, image_factory)

        return img

    def create_text_wrapper(self):
        text_wrapper = Element("span")
        text_wrapper.add_class("text_wrapper")
        text_wrapper.append(self.get_label())
        return text_wrapper

    def get_label(self):
        return any_translation(
            self.item,
            language_chain = self.language_chain,
            referer = self.referer
        )

