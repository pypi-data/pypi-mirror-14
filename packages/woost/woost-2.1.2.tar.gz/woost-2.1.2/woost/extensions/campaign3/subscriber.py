#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema


class Subscriber(schema.SchemaObject):

    members_order = ["subscriber_name", "subscriber_email"]

    subscriber_name = schema.String(
        required = True
    )

    subscriber_email = schema.EmailAddress(
        required = True
    )

