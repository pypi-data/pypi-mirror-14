#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail.pkgutils import resolve
from woost.controllers.basecmscontroller import BaseCMSController
from woost.extensions.payments.paymentgateway import PaymentGateway


class PaymentRootController(BaseCMSController):
    """Root controller for all payment related requests.

    This controller does nothing by itself, it merely identifies the payment
    gateway that should handle an incomming request and forwards the request to
    the gateway's controller (an instance of L{PaymentGatewayController}).
    """

    def resolve(self, path):

        if not path:
            raise cherrypy.NotFound()

        # Identify the gateway involved in the payment
        gateway_id = path.pop(0)

        try:
            gateway_id = int(gateway_id)
        except:
            raise cherrypy.HTTPError(400)

        gateway = PaymentGateway.get_instance(gateway_id)

        if gateway is None:
            raise cherrypy.NotFound()

        # Forward the request to the gateway's controller
        controller_class = resolve(gateway.payment_gateway_controller_class)
        return controller_class(gateway)

