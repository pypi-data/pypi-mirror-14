#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.controllers.backoffice.useractions import UserAction
from woost.extensions.surveys.survey import Survey


class SurveyResultsAction(UserAction):

    min = 1
    max = 1
    content_type = Survey
    included = frozenset(["toolbar", "item_buttons"])


SurveyResultsAction("survey_results").register()

