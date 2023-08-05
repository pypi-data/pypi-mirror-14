#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from cocktail.translations import translations
from woost.models import Website, Publishable
from woost.extensions.ecommerce.ecommercebillingconcept \
    import ECommerceBillingConcept
from woost.extensions.payments import PaymentsExtension
from woost.extensions.payments.paymentgateway import PaymentGateway


Website.add_member(
    schema.Collection(
        "ecommerce_payment_types",
        items = schema.String(
            enumeration = ("payment_gateway", "transfer", "cash_on_delivery"),
            translate_value = lambda value, language = None, **kwargs:
                translations(
                    "Website.ecommerce_payment_types=%s" % value,
                    language = language
                ),
        ),
        min = 1,
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Collection(
        "ecommerce_pricing",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(),
        integral = True,
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Collection(
        "ecommerce_shipping_costs",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(),
        integral = True,
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Collection(
        "ecommerce_taxes",
        items = schema.Reference(type = ECommerceBillingConcept),
        related_end = schema.Collection(),
        integral = True,
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Reference(
        "ecommerce_default_catalog",
        type = Publishable,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Collection(
        "ecommerce_order_steps",
        items = schema.Reference(type = Publishable),
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "ecommerce"
    )
)

Website.add_member(
    schema.Collection(
        "ecommerce_orders",
        items = "woost.extensions.ecommerce.ecommerceorder."
                "ECommerceOrder",
        bidirectional = True,
        visible = False,
        member_group = "ecommerce"
    )
)

Website.members_order += [
    "ecommerce_payment_types",
    "ecommerce_pricing",
    "ecommerce_shipping_costs",
    "ecommerce_taxes",
    "ecommerce_default_catalog",
    "ecommerce_order_steps"
]

payments_ext = PaymentsExtension.instance

if payments_ext.enabled:
    Website.add_member(
        schema.Reference(
            "ecommerce_payment_gateway",
            type = PaymentGateway,
            required = True,
            related_end = schema.Collection(),
            listed_by_default = False,
            member_group = "ecommerce"
        )
    )

    Website.members_order += [
        "ecommerce_payment_gateway"
    ]

