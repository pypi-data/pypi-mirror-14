#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item


class AudioDecoder(Item):

    instantiable = True
    visible_from_root = False

    mime_type = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = False,
        descriptive = True
    )

    command = schema.String(
        required = True
    )

