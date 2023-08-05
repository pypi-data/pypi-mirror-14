#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail.controllers import (
    request_property,
    Form
)
from woost import app
from woost.controllers.notifications import pop_user_notifications


class OrderStepForm(Form):

    @request_property
    def order_steps(self):
        return app.website.ecommerce_order_steps

    @request_property
    def current_step(self):
        return app.publishable

    @request_property
    def next_step(self):
        steps = self.order_steps
        pos = steps.index(self.current_step)
        if pos + 1 < len(steps):
            return steps[pos + 1]

    def proceed(self):
        pop_user_notifications()
        next_step = self.next_step
        if next_step is not None:
            raise cherrypy.HTTPRedirect(next_step.get_uri())


class ProceedForm(OrderStepForm):

    actions = "proceed",

    def after_submit(self):
        self.proceed()

