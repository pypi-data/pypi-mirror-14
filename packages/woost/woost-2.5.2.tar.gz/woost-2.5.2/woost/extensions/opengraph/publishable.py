#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.iteration import first
from cocktail.translations import translations
from cocktail.html.datadisplay import display_factory
from woost.models import Publishable, Document, News, File
from woost.extensions.opengraph.opengraphtype import OpenGraphType
from woost.extensions.opengraph.utils import (
    export_content,
    get_publishable_website
)

File.default_open_graph_enabled = False
File.default_open_graph_type = None

Publishable.members_order += [
    "open_graph_enabled",
    "open_graph_type"
]

Publishable.add_member(
    schema.Boolean("open_graph_enabled",
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "meta.open_graph"
    )
)

Publishable.add_member(
    schema.Reference("open_graph_type",
        type = OpenGraphType,
        required = Publishable["open_graph_enabled"],
        related_end = schema.Collection(
            block_delete = True
        ),
        default = schema.DynamicDefault(
            lambda: OpenGraphType.get_instance(code = "article")
        ),
        indexed = True,
        listed_by_default = False,
        member_group = "meta.open_graph",
        edit_control = display_factory(
            "cocktail.html.DropdownSelector",
            grouping = lambda type: type.category
        )
    )
)

def _get_publishable_properties(self):

    properties = {
        "og:title": translations(self),
        "og:type": self.open_graph_type.code,
        "og:url": self.get_uri(host = ".")
    }

    description = self.get_open_graph_description()
    if description:
        properties["og:description"] = description

    image = self.get_open_graph_image()
    if image:
        if isinstance(image, Publishable):
            if image.is_accessible():
                image = image.get_image_uri("facebook", host = ".")
            else:
                image = None

        if image:
            properties["og:image"] = image

    video = self.get_open_graph_video()
    if video:
        if isinstance(video, Publishable):
            video = video.get_uri(host = ".")
        properties["og:video"] = video

    return properties

Publishable.get_open_graph_properties = _get_publishable_properties

def _get_publishable_description(self):
    website = get_publishable_website(self)
    if website:
        return website.description

Publishable.get_open_graph_description = _get_publishable_description

def _get_document_description(self):
    if self.description:
        return export_content(self.description)

    return Publishable.get_open_graph_description(self)

Document.get_open_graph_description = _get_document_description

def _get_news_description(self):

    if self.summary:
        return export_content(self.summary)

    return Document.get_open_graph_description(self)

News.get_open_graph_description = _get_news_description

def _get_publishable_open_graph_image(self):
    website = get_publishable_website(self)
    if website:
        return website.logo

Publishable.get_open_graph_image = _get_publishable_open_graph_image

def _get_publishable_open_graph_video(self):
    return None

Publishable.get_open_graph_video = _get_publishable_open_graph_video

def _get_news_open_graph_image(self):
    return self.image

News.get_open_graph_image = _get_news_open_graph_image

# Metadata for shop products (only if the 'shop' extension is enabled)
from woost.extensions.shop import ShopExtension

if ShopExtension.instance.enabled:
    from woost.extensions.shop.product import Product
    Product.default_open_graph_type = schema.DynamicDefault(
        lambda: OpenGraphType.get_instance(code = "product")
    )

