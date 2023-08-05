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
from woost.models import Block, ElementType
from woost.extensions.ecommerce.ecommerceproduct import ECommerceProduct


class ECommerceProductListing(Block):

    max_page_size = 50

    instantiable = True
    type_group = "blocks.ecommerce"
    block_display = "woost.extensions.ecommerce.ProductListingDisplay"

    groups_order = list(Block.groups_order)
    groups_order.insert(groups_order.index("content") + 1, "listing")

    members_order = [
        "element_type",
        "products",
        "item_accessibility",
        "listing_order",
        "paginated",
        "page_size",
        "view_class"
    ]

    default_controller = "woost.extensions.ecommerce" \
        ".ecommerceproductlistingcontroller.ECommerceProductListingController"

    element_type = ElementType(
        member_group = "content"
    )

    products = schema.Collection(
        items = schema.Reference(type = ECommerceProduct),
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
        enumeration = [
            "arbitrary",
            "-last_update_time",
            "price",
            "-price"
        ],
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
            "woost.extensions.ecommerce.CompactProductListing",
            "woost.extensions.ecommerce.TextAndImageProductListing"
        ],
        default = "woost.extensions.ecommerce.TextAndImageProductListing",
        member_group = "listing"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.tag = self.element_type
        view.name_prefix = self.name_prefix
        view.name_suffix = self.name_suffix

        if not self.products:
            view.depends_on(ECommerceProduct)

        if self.paginated:
            view.pagination = self.pagination
        else:
            view.products = self.select_products()

    def select_products(self):

        if self.item_accessibility == "accessible":
            products = ECommerceProduct.select_accessible()
        elif self.item_accessibility == "published":
            products = ECommerceProduct.select_published()
        elif self.item_accessibility == "any":
            products = ECommerceProduct.select()

        if self.products:
            products.base_collection = self.products

        self._apply_order(products)
        return products

    def _apply_order(self, products):
        if self.listing_order != "arbitrary":
            products.add_order(self.listing_order)

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
            "items": self.select_products()
        })

