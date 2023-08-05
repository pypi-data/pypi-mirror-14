#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema


class MetaTags(schema.Collection):

    def __init__(self, *args, **kwargs):
        kwargs["items"] = schema.Tuple(
            items = (
                schema.String("key", required = True),
                schema.String("value")
            ),
            request_value_separator = "="
        )
        kwargs.setdefault("searchable", False)
        kwargs.setdefault("edit_control", "cocktail.html.TextArea")
        kwargs.setdefault("request_value_separator", "\n")
        schema.Collection.__init__(self, *args, **kwargs)

