#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .document import Document
from .template import Template
from .slot import Slot


class Page(Document):

    default_template = schema.DynamicDefault(
        lambda: Template.get_instance(qname = "woost.standard_template")
    )

    blocks = Slot()

