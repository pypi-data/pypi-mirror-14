#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail import schema
from cocktail.controllers import (
    Controller,
    request_property,
    FormProcessor
)
from woost.models import Publishable, get_current_website
from woost.extensions.ecommerce.basket import Basket
from woost.extensions.ecommerce.ecommerceorder import ECommerceOrder
from woost.extensions.ecommerce.orderstepcontroller import ProceedForm
from woost.extensions.payments import PaymentsExtension


class SummaryController(FormProcessor, Controller):

    is_transactional = True

    class SubmitOrderForm(ProceedForm):

        order = None

        @request_property
        def errors(self):
            return schema.ErrorList(ECommerceOrder.get_errors(Basket.get()))

        def submit(self):
            ProceedForm.submit(self)
            self.order = Basket.pop()
            self.order.status = "payment_pending"
            self.order.update_cost()

        def after_submit(self):
            payments = PaymentsExtension.instance
            website = get_current_website()
            payment_gateway = website.ecommerce_payment_gateway

            # Redirect the user to the payment gateway
            if payments.enabled \
            and payment_gateway \
            and self.order.payment_type == "payment_gateway":
                payment_gateway.initiate_payment(self.order.id)

            # No payment gateway available, redirect the user to the success
            # page; the payment will have to be handled manually by the site's
            # personnel
            else:
                raise cherrypy.HTTPRedirect(
                    Publishable.require_instance(
                        qname = "woost.extensions.ecommerce.success_page"
                    ).get_uri(
                        parameters = {"order": self.order.id}
                    )
                )

    @request_property
    def checkout_schema(self):
        return Basket.get().get_public_schema()

    @request_property
    def output(self):
        output = Controller.output(self)
        output["checkout_schema"] = self.checkout_schema
        return output

