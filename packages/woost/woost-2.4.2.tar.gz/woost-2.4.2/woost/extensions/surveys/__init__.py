#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension


translations.define("SurveysExtension",
    ca = u"Enquestes",
    es = u"Encuestas",
    en = u"Surveys"
)

translations.define("SurveysExtension-plural",
    ca = u"Enquestes",
    es = u"Encuestas",
    en = u"Surveys"
)


class SurveysExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet fer enquestes als visitants de la web.""",
            "ca"
        )
        self.set("description",
            u"""Permite hacer encuestas a los visitantes de la web.""",
            "es"
        )
        self.set("description",
            u"""Design and conduct surveys for the visitors of the website.""",
            "en"
        )

    def _load(self):
        from woost.extensions.surveys import (
            strings,
            survey,
            surveyblock,
            surveyresultsaction
        )

        from woost.controllers.backoffice.itemcontroller import ItemController
        from woost.extensions.surveys.surveyresultscontroller \
            import SurveyResultsController

        ItemController.survey_results = SurveyResultsController

