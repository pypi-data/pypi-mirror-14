#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Configuration, LocaleMember


Configuration.add_member(
    schema.Mapping("translation_workflow_paths",
        keys = LocaleMember(
            "source_language",
            required = True
        ),
        values = schema.Collection(
            "target_languages",
            items = LocaleMember(
                required = True
            ),
            min = 1
        ),
        edit_control = "cocktail.html.TextArea",
        request_items_separator = "\n",
        member_group = "language"
    )
)

