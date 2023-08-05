#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2009
"""
from decimal import Decimal
from cocktail import schema
from cocktail.translations import translations
from woost.models import (
    Publishable,
    Controller,
    File,
    Slot,
    get_current_website
)


class ECommerceProduct(Publishable):

    instantiable = False
    type_group = "ecommerce"

    members_order = [
        "image",
        "description",
        "price",
        "weight",
        "purchase_model",
        "purchases"
    ]

    default_controller = schema.DynamicDefault(
        lambda: Controller.get_instance(
            qname = "woost.extensions.ecommerce.product_controller"
        )
    )

    image = schema.Reference(
        type = File,
        related_end = schema.Collection(),
        relation_constraints = {"resource_type": "image"},
        member_group = "product_data"
    )

    description = schema.String(
        translated = True,
        edit_control = "woost.views.RichTextEditor",
        member_group = "product_data",
        listed_by_default = False
    )

    price = schema.Money(
        required = True,
        indexed = True,
        default = Decimal("0"),
        member_group = "product_data"
    )

    weight = schema.Decimal(
        translate_value = lambda value, language = None, **kwargs:
            "" if not value else "%s Kg" % translations(value, language),
        member_group = "product_data"
    )

    purchase_model = schema.Reference(
        class_family = "woost.extensions.ecommerce.ecommercepurchase."
                       "ECommercePurchase",
        default = schema.DynamicDefault(
            lambda: ECommerceProduct.purchase_model.class_family
        ),
        required = True,
        searchable = False,
        member_group = "product_data",
        listed_by_default = False
    )

    purchases = schema.Collection(
        items = "woost.extensions.ecommerce.ecommercepurchase."
                "ECommercePurchase",
        bidirectional = True,
        visible = False,
        member_group = "product_data"
    )

    blocks = Slot()

    def offers(self):
        website = get_current_website()
        for pricing in website.ecommerce_pricing:
            if not pricing.hidden and pricing.applies_to(self):
                yield pricing

