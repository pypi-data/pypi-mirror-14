#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from woost.models import Document
from tpv.paypal import PayPalPaymentGateway as Implementation
from woost.extensions.payments.paymentgateway import PaymentGateway


class PayPalPaymentGateway(PaymentGateway, Implementation):

    instantiable = True

    default_label = schema.DynamicDefault(
        lambda: translations("PayPalPaymentGateway.label default")
    )

    members_order = [
        "business",
        "payment_successful_page",
        "payment_failed_page"
    ]

    business = schema.String(
        required = True,
        shadows_attribute = True,
        text_search = False
    )

    payment_successful_page = schema.Reference(
        type = Document,
        related_end = schema.Reference()
    )

    payment_failed_page = schema.Reference(
        type = Document,
        related_end = schema.Reference()
    )

    def get_payment_successful_url(self, payment):
        if self.payment_successful_page:
            return self.payment_successful_page.get_uri(
                host = "!",
                parameters = {"payment_id": payment.id}
            )

    def get_payment_failed_url(self, payment):
        if self.payment_failed_page:
            return self.payment_failed_page.get_uri(
                host = "!",
                parameters = {"payment_id": payment.id}
            )

