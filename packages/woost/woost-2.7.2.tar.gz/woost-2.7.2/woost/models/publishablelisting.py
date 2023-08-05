#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from cocktail.controllers import (
    request_property,
    get_parameter,
    Pagination
)
from .block import Block
from .elementtype import ElementType
from .publishable import Publishable


class PublishableListing(Block):

    max_page_size = 50

    instantiable = True
    type_group = "blocks.listings"
    block_display = "woost.views.PublishableListingDisplay"

    groups_order = list(Block.groups_order)
    groups_order.insert(groups_order.index("content") + 1, "listing")

    members_order = [
        "element_type",
        "publishables",
        "item_accessibility",
        "listing_order",
        "links_open_in_new_window",
        "links_force_download",
        "paginated",
        "page_size",
        "view_class"
    ]

    element_type = ElementType(
        member_group = "content"
    )

    publishables = schema.Collection(
        items = schema.Reference(type = Publishable),
        related_end = schema.Collection(),
        invalidates_cache = True,
        member_group = "listing"
    )

    item_accessibility = schema.String(
        required = True,
        enumeration = [
            "accessible",
            "published",
            "any"
        ],
        default = "accessible",
        member_group = "listing"
    )

    listing_order = schema.String(
        default = "arbitrary",
        enumeration = ["arbitrary", "-last_update_time"],
        member_group = "listing"
    )

    links_open_in_new_window = schema.Boolean(
        required = True,
        default = False,
        member_group = "listing"
    )

    links_force_download = schema.Boolean(
        required = True,
        default = False,
        member_group = "listing"
    )

    paginated = schema.Boolean(
        required = True,
        default = False,
        member_group = "listing"
    )

    page_size = schema.Integer(
        min = 1,
        required = paginated,
        member_group = "listing"
    )

    view_class = schema.String(
        required = True,
        shadows_attribute = True,
        enumeration = [
            "woost.views.PublishableTextualListing",
            "woost.views.PublishableIconListing",
            "woost.views.PublishableGrid",
            "woost.views.PublishableCollage"
        ],
        default = "woost.views.PublishableTextualListing",
        member_group = "listing"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.tag = self.element_type
        view.name_prefix = self.name_prefix
        view.name_suffix = self.name_suffix
        view.links_open_in_new_window = self.links_open_in_new_window
        view.links_force_download = self.links_force_download

        if not self.publishables:
            view.depends_on(Publishable)

        if self.paginated:
            view.pagination = self.pagination
        else:
            view.publishables = self.select_publishables()

    def select_publishables(self):

        if self.item_accessibility == "accessible":
            publishables = Publishable.select_accessible()
        elif self.item_accessibility == "published":
            publishables = Publishable.select_published()
        elif self.item_accessibility == "any":
            publishables = Publishable.select()

        publishables.base_collection = self.publishables
        self._apply_order(publishables)
        return publishables

    def _apply_order(self, publishables):
        if self.listing_order != "arbitrary":
            publishables.add_order(self.listing_order)

    @request_property
    def pagination(self):
        return get_parameter(
            self.pagination_member,
            errors = "set_default",
            prefix = self.name_prefix,
            suffix = self.name_suffix
        )

    @request_property
    def pagination_member(self):
        return Pagination.copy(**{
            "page_size.default": self.page_size,
            "page_size.max": self.max_page_size,
            "items": self.select_publishables()
        })

