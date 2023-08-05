#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2009
"""
import cherrypy
from decimal import Decimal
from simplejson import dumps
from cocktail.modeling import underscore_to_capital
from cocktail.translations import (
    translations,
    set_language,
    language_context
)
from cocktail import schema
from cocktail.persistence import datastore
from woost.models import (
    Configuration,
    Extension,
    Publishable,
    Page,
    Template,
    Controller,
    EmailTemplate,
    User,
    TextBlock,
    CustomBlock
)
from woost.models.rendering import ImageFactory, Thumbnail
from woost.models.triggerresponse import SendEmailTriggerResponse
from woost.controllers import CMSController

translations.define("ECommerceExtension",
    ca = u"Comerç online",
    es = u"Comercio online",
    en = u"E-commerce"
)

translations.define("ECommerceExtension-plural",
    ca = u"Comerç online",
    es = u"Comercio online",
    en = u"E-commerce"
)


class ECommerceExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet vendre productes des del lloc web.""",
            "ca"
        )
        self.set("description",
            u"""Permite vender productos des del sitio web.""",
            "es"
        )
        self.set("description",
            u"""Allows selling products online.""",
            "en"
        )

    def _load(self):

        from woost.extensions.ecommerce import (
            strings,
            typegroups,
            website,
            ecommerceproduct,
            ecommerceorder,
            ecommercepurchase,
            ecommercebillingconcept,
            ecommerceordercompletedtrigger,
            orderstepscontainerblock,
            ecommerceproductlisting,
        )

        # If the payments extension is enabled, setup the payment gateway for
        # the shop
        from woost.extensions.payments import PaymentsExtension
        payments_ext = PaymentsExtension.instance

        if payments_ext.enabled:
            self._setup_payment_gateway()

        self._setup_ecommerce_state()

        # Create the pages for the shop the first time the extension runs
        self.install()

    def _setup_ecommerce_state(self):

        from woost.extensions.ecommerce.basket import Basket

        @cherrypy.expose
        def ecommerce_state(self):

            cherrypy.response.headers["Content-Type"] = "text/javascript"
            order = Basket.get(create_new = False)
            if order:
                order.update_cost()

            def format_amount(amount):
                return str(amount.quantize(Decimal("1.00")))

            return "cocktail.declare('woost.ecommerce'); woost.ecommerce = %s;" % dumps(
                {
                    "order": {
                        "id": order.id,
                        "total": format_amount(order.total),
                        "count_label": translations(
                            "woost.extensions.ecommerce.BasketIndicator",
                            count = order.count_units()
                        ),
                        "purchases": [{
                            "id": purchase.id,
                            "product": {
                                "id": purchase.product.id,
                                "label": translations(purchase.product)
                            },
                            "quantity": purchase.quantity,
                            "total": format_amount(purchase.total)
                        }
                        for purchase in order.purchases]
                    }
                }
                if order else {
                    "order": {
                        "count_label": translations(
                            "woost.extensions.ecommerce.BasketIndicator",
                            count = 0
                        )
                    }
                }
            )

        CMSController.ecommerce_state = ecommerce_state

    def _setup_payment_gateway(self):

        from tpv import (
            Currency,
            Payment,
            PaymentItem,
            PaymentNotFoundError
        )
        from woost.extensions.payments.paymentgateway import PaymentGateway
        from woost.extensions.payments.transactionnotifiedtrigger \
            import launch_transaction_notification_triggers
        from woost.extensions.ecommerce.ecommerceorder import ECommerceOrder
        from woost.extensions.payments import PaymentsExtension
        from woost.extensions.payments.paypal import PayPalPaymentGateway

        ecommerce_ext = self

        def get_payment(self, payment_id):

            order = ECommerceOrder.get_instance(int(payment_id))

            if order is None:
                raise PaymentNotFoundError(payment_id)

            payment = Payment()
            payment.id = order.id
            payment.description = order.get_description_for_gateway()
            payment.amount = order.total
            payment.order = order
            payment.currency = Currency(self.currency)

            # PayPal form data
            if isinstance(self, PayPalPaymentGateway):
                paypal_form_data = {}
                if order.address:
                    paypal_form_data["address1"] = order.address

                if order.town:
                    paypal_form_data["city"] = order.town

                if order.country and order.country.code:
                    paypal_form_data["country"] = order.country.code

                if order.postal_code:
                    paypal_form_data["zip"] = order.postal_code

                if order.language:
                    paypal_form_data["lc"] = order.language

                payment.paypal_form_data = paypal_form_data

            for purchase in order.purchases:
                payment.add(PaymentItem(
                    reference = str(purchase.product.id),
                    description = translations(purchase.product),
                    units = purchase.quantity,
                    price = purchase.total
                ))

            return payment

        PaymentGateway.get_payment = get_payment

        def receive_order_payment(event):
            payment = event.payment
            order = payment.order
            set_language(order.language)
            order.status = payment.status
            order.gateway_parameters = payment.gateway_parameters

        def commit_order_payment(event):
            datastore.commit()

        events = PaymentGateway.transaction_notified
        pos = events.index(launch_transaction_notification_triggers)
        events.insert(pos, receive_order_payment)
        events.insert(pos + 2, commit_order_payment)

    def _install(self):

        from woost.extensions.ecommerce.ecommerceproductlisting import ECommerceProductListing

        website = Configuration.instance.websites[0]

        catalog = self._create_document("catalog")
        catalog.blocks.append(ECommerceProductListing())
        catalog.insert()
        website.ecommerce_default_catalog = catalog

        for child_name in (
            "basket",
            "checkout",
            "summary"
        ):
            child = self._create_document(child_name)
            self.__add_ecommerce_step_blocks(child, child_name)
            child.hidden = True
            child.parent = catalog
            child.insert()
            website.ecommerce_order_steps.append(child)

        for child_name in (
            "success",
            "failure"
        ):
            child = self._create_document(child_name)
            child.hidden = True
            child.parent = catalog
            child.insert()

        self._create_controller("product").insert()
        self._create_ecommerceorder_completed_trigger().insert()
        self._create_incoming_order_trigger().insert()
        self._create_image_factories()

    def _create_document(self, name,
        cls = Page,
        template = None,
        controller = None):

        document = cls()
        document.qname = "woost.extensions.ecommerce.%s_page" % name

        self.__translate_field(document, "title")

        if isinstance(document, Page):
            self.__add_text_block(document, "body")

        return document

    def _create_controller(self, name):
        controller = Controller( )
        controller.qname = "woost.extensions.ecommerce.%s_controller" % name
        self.__translate_field(controller, "title")
        controller.python_name = \
            "woost.extensions.ecommerce.%scontroller.%sController" % (
                name,
                underscore_to_capital(name)
            )
        return controller

    def _create_ecommerceorder_completed_trigger(self):
        from woost.extensions.ecommerce.ecommerceordercompletedtrigger import \
            ECommerceOrderCompletedTrigger
        trigger = ECommerceOrderCompletedTrigger( )
        trigger.qname = \
            "woost.extensions.ecommerce.ecommerceorder_completed_trigger"
        self.__translate_field(trigger, "title")
        Configuration.instance.triggers.append(trigger)
        trigger.condition = "target.customer and not target.customer.anonymous and target.customer.email"
        trigger.matching_items = {'type': u'woost.extensions.ecommerce.ecommerceorder.ECommerceOrder'}

        # EmailTemplate
        template = EmailTemplate()
        template.qname = \
            "woost.extensions.ecommerce.ecommerceorder_completed_emailtemplate"
        self.__translate_field(template, "title")
        template.sender = '"%s"' % User.require_instance(
            qname = "woost.administrator"
        ).email
        template.receivers = '[items[0].customer.email]'
        template.initialization_code = """
from woost.models import Configuration
logo = Configuration.instance.get_setting("logo")
if logo:
    attachments["logo"] = logo
"""
        template.template_engine = "mako"

        for language in Configuration.instance.languages:
            with language_context(language):
                template.subject = template.title
                template.body = """
<%
from cocktail.controllers import Location
from cocktail.html import templates

order = items[0]
order_summary = templates.new("woost.extensions.ecommerce.OrderConfirmationMessage")
order_summary.order = order
%>

<html>
    <head>
        <base href="@{unicode(Location.get_current_host())}"/>
    </head>
    <body>
        ${order_summary.render()}
    </body>
</html>
"""

        # Response
        response = SendEmailTriggerResponse()
        response.qname = \
            "woost.extensions.ecommerce.ecommerceorder_completed_response"
        response.email_template = template

        trigger.responses = [response]
        return trigger

    def _create_incoming_order_trigger(self):
        from woost.extensions.ecommerce.incomingordertrigger import \
            IncomingOrderTrigger
        trigger = IncomingOrderTrigger( )
        trigger.qname = "woost.extensions.ecommerce.incoming_order.trigger"
        self.__translate_field(trigger, "title")
        Configuration.instance.triggers.append(trigger)
        trigger.matching_items = {'type': u'woost.extensions.ecommerce.ecommerceorder.ECommerceOrder'}

        # EmailTemplate
        template = EmailTemplate()
        template.qname = \
            "woost.extensions.ecommerce.incoming_order.email_template"
        self.__translate_field(template, "title")
        admin = User.require_instance(qname = "woost.administrator")
        template.sender = repr(admin.email)
        template.receivers = repr([admin.email])
        template.template_engine = "mako"

        for language in Configuration.instance.languages:
            with language_context(language):
                template.subject = template.title
                template.body = """
<%
from cocktail.translations import translations
from woost.models import Publishable

order = items[0]
bo = Publishable.require_instance(qname = "woost.backoffice")
edit_url = bo.get_uri(host = ".", path = ["content", str(order.id)])
%>

<html>
    <body>
        <a href="${edit_url}">${translations('woost.extensions.ecommerce.incoming_order.edit_link')}
        </a>
    </body>
</html>
"""

        # Response
        response = SendEmailTriggerResponse()
        response.email_template = template
        trigger.responses = [response]

        return trigger

    def _create_image_factories(self):
        thumbnail = ImageFactory()
        thumbnail.qname = \
            "woost.extensions.ecommerce.ecommerce_basket_thumbnail"
        self.__translate_field(thumbnail, "title")
        thumbnail.identifier = "ecommerce_basket_thumbnail"
        thumbnail.effects = [Thumbnail(width = "75", height = "75")]
        thumbnail.insert()

    def __translate_field(self, obj, key):
        for language in Configuration.instance.languages:
            with language_context(language):
                value = translations("%s.%s" % (obj.qname, key))
                if value:
                    obj.set(key, value)

    def __add_text_block(
        self,
        document,
        key,
        style = None,
        element_type = None,
        slot = "blocks"
    ):
        block = TextBlock()
        if slot:
            blocks = document.get(slot)
        else:
            blocks = document.blocks

        has_text = False
        for language in Configuration.instance.languages:
            with language_context(language):
                value = translations("%s.%s" % (document.qname, key))
                if value:
                    block.set("text", value)
                    has_text = True

        if not has_text:
            return

        if element_type:
            block.element_type = element_type

        if style:
            block.styles.append(style)

        blocks.append(block)
        block.insert()

    def __add_ecommerce_step_blocks(
        self,
        document,
        key
    ):
        from woost.extensions.ecommerce.orderstepscontainerblock import \
        OrderStepsContainerBlock

        order_steps = OrderStepsContainerBlock()
        block = CustomBlock()
        block.qname = "woost.extensions.ecommerce.%s_block" % key
        self.__translate_field(block, "heading")
        block.view_class = \
            "woost.extensions.ecommerce.%sBlockView" % key.capitalize()
        block.controller = \
            "woost.extensions.ecommerce.%scontroller.%sController" % (
                key, key.capitalize()
            )
        order_steps.blocks.append(block)
        document.blocks.append(order_steps)
        order_steps.insert()

