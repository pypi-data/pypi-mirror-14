#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost import app
from woost.controllers.publishablecontroller import PublishableController


class TextFileController(PublishableController):

    def _produce_content(self, **kwargs):
        return app.publishable.content

