#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Block, Publishable
from woost.extensions.surveys.survey import Survey


class SurveyBlock(Block):

    type_group = "blocks.forms"
    view_class = "woost.extensions.surveys.SurveyView"
    default_controller = \
        "woost.extensions.surveys.surveycontroller.SurveyController"

    members_order = [
        "survey",
        "redirection"
    ]

    survey = schema.Reference(
        type = Survey,
        related_end = schema.Collection(),
        required = True,
        member_group = "content"
    )

    redirection = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.survey = self.survey

