#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.controllers import (
    Controller,
    request_property,
    Form,
    FormProcessor
)
from woost import app
from woost.extensions.ecommerce.basket import Basket
from woost.extensions.ecommerce.orderstepcontroller import ProceedForm


class CheckoutController(FormProcessor, Controller):

    class CheckoutForm(ProceedForm):

        @request_property
        def model(self):
            return Basket.get().get_public_schema()

        @request_property
        def source_instance(self):
            return Basket.get()

        @request_property
        def schema(self):
            schema = ProceedForm.schema(self)
            payment_type = schema.get_member("payment_type")
            if payment_type:
                payment_type.enumeration = \
                    app.website.ecommerce_payment_types
            return schema

        def submit(self):
            ProceedForm.submit(self)
            Basket.store()

