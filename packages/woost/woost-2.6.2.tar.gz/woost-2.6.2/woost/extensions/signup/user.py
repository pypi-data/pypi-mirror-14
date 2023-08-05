#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import User


User.add_member(
    schema.Boolean(
        "confirmed_email",
        default = False,
        required = True
    )
)

