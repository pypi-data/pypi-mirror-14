#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
"""
from cocktail import schema
from .document import Document
from .slot import Slot
from .file import File


class Event(Document):

    members_order = [
        "event_start",
        "event_end",
        "event_location",
        "image",
        "summary",
        "blocks"
    ]

    event_start = schema.DateTime(
        member_group = "content",
        indexed = True
    )

    event_end = schema.DateTime(
        member_group = "content",
        min = event_start,
        indexed = True
    )

    event_location = schema.String(
        edit_control = "cocktail.html.TextArea",
        translated = True,
        member_group = "content"
    )

    image = schema.Reference(
        type = File,
        relation_constraints = {"resource_type": "image"},
        listed_by_default = False,
        member_group = "content"
    )

    summary = schema.String(
        translated = True,
        edit_control = "woost.views.RichTextEditor",
        listed_by_default = False,
        member_group = "content"
    )

    blocks = Slot()

