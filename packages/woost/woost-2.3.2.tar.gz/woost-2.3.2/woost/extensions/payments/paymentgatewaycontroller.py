#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from woost.controllers.basecmscontroller import BaseCMSController


class PaymentGatewayController(BaseCMSController):

    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway
        BaseCMSController.__init__(self)

    def __call__(self, *args, **kwargs):
        raise cherrypy.NotFound()

    @cherrypy.expose
    def handshake(self, **parameters):
        return self.payment_gateway.handle_handshake(parameters)

    @cherrypy.expose
    def notification(self, **parameters):
        payment = self.payment_gateway.process_notification(parameters)
        self.payment_gateway.transaction_notified(payment = payment)

