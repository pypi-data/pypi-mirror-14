#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from cocktail.controllers import (
    request_property,
    get_parameter,
    Controller,
    FormProcessor,
    Form
)
from woost.extensions.ecommerce.ecommerceproduct import ECommerceProduct
from woost.extensions.ecommerce.productcontroller import ProductController


class ECommerceProductListingController(FormProcessor, Controller):

    class AddProductForm(ProductController.AddProductForm):

        @request_property
        def product(self):
            return get_parameter(
                schema.Reference(
                    "product",
                    type = ECommerceProduct,
                    required = True
                )
            )

        @request_property
        def model(self):
            return self.product \
                and self.product.purchase_model \
                or Form.model(self)

        @request_property
        def adapter(self):
            return self.product \
                and ProductController.AddProductForm.adapter(self) \
                or Form.adapter(self)

        def create_instance(self):
            return self.product \
                and ProductController.AddProductForm.create_instance(self) \
                or Form.create_instance(self)

