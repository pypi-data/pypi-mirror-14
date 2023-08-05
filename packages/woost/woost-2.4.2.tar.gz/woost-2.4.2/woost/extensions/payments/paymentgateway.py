#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2009
"""
from tpv.currencies import currency_alpha
from cocktail.modeling import OrderedDict
from cocktail.events import Event
from cocktail.translations import translations, get_language
from cocktail import schema
from cocktail.controllers import Location
from woost.models import Item, get_current_website


class PaymentGateway(Item):

    instantiable = False
    visible_from_root = False
    payment_gateway_controller_class = \
        "woost.extensions.payments.paymentgatewaycontroller.PaymentGatewayController"

    transaction_notified = Event(
        """An event triggered when the payment gateway notifies the application
        of the outcome of a payment transaction.

        @param payment: The payment that the notification is sent for.
        @type payment: L{Payment<tpv.payment.Payment>}
        """
    )

    members_order = [
        "label",
        "test_mode",
        "currency"
    ]

    label = schema.String(
        required = True,
        translated = True
    )

    test_mode = schema.Boolean(
        required = True,
        default = True
    )

    currency = schema.String(
        required = True,
        enumeration = currency_alpha,
        translatable_enumeration = False,
        text_search = False
    )

    def __translate__(self, language, **kwargs):
        return translations(self.__class__.name, language)

    def initiate_payment(self, payment_id):
        """Begin a payment transaction, redirecting the user to the payment
        gateway.

        @param payment_id: The identifier of the payment to execute.
        """
        url, params = self.get_payment_form_data(payment_id, get_language())

        location = Location(url)
        location.method = "POST"
        location.form_data = OrderedDict(params)
        location.go()

    def get_payment_url(self, *args, **kwargs):

        website = get_current_website()
        location = Location()
        location.relative = False

        if website.https_policy != "never":
            location.scheme = "https"

        location.host = website.hosts[0]
        location.path_info = "payments/" + str(self.id)
        location.join_path(*args)
        location.query_string.update(kwargs)

        return unicode(location)

    @property
    def handshake_url(self):
        return self.get_payment_url("handshake")

    @property
    def notification_url(self):
        return self.get_payment_url("notification")

