#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item


class TranslationWorkflowComment(Item):

    type_group = "translation_workflow"
    instantiable = False
    visible_from_root = False

    members_order = [
        "request",
        "text"
    ]

    request = schema.Reference(
        type = "woost.extensions.translationworkflow.request."
               "TranslationWorkflowRequest",
        bidirectional = True,
        required = True,
        editable = schema.NOT_EDITABLE
    )

    text = schema.HTML(
        required = True,
        descriptive = True,
        spellcheck = True
    )

