#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from cocktail import schema
from woost.models import User

User.add_member(
    schema.String("facebook_user_id",
        indexed = True,
        unique = True,
        editable = schema.READ_ONLY,
        listed_by_default = False
    )
)

