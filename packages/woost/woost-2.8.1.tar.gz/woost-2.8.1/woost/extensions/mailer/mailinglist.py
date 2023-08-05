#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import Item


class MailingList(Item):

    members_order = ["title", "mailings"]

    title = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        spellcheck = True
    )

    users = schema.Collection(
        items = "woost.models.User",
        bidirectional = True,
        listed_by_default = False
    )

    mailings = schema.Collection(
        items = "woost.extensions.mailer.mailing.Mailing",
        bidirectional = True,
        editable = schema.NOT_EDITABLE,
        listed_by_default = False
    )

