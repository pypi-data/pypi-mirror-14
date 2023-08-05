#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema
from cocktail.persistence import PersistentList, PersistentMapping
from cocktail.html import templates
from woost.models import Item


class Survey(Item):

    members_order = [
        "title",
        "questions"
    ]

    title = schema.String(
        translated = True,
        required = True,
        indexed = True,
        unique = True,
        normalized_index = True,
        spellcheck = True,
        descriptive = True
    )

    questions = schema.Collection(
        items = "woost.extensions.surveys.survey.SurveyQuestion",
        bidirectional = True,
        integral = True,
        min = 1
    )

    def __init__(self, *args, **kwargs):
        Item.__init__(self, *args, **kwargs)
        self.__submissions = PersistentList()

    @property
    def submissions(self):
        return self.__submissions

    def add_submission(self, submission):
        self.__submissions.append(
            PersistentMapping(dict(submission))
        )

    def create_survey_schema(self):
        survey_schema = schema.Schema("SurveyForm")
        for question in self.questions:
            if question.active:
                question.init_survey_schema(survey_schema)
        return survey_schema


class SurveyQuestion(Item):

    instantiable = False
    visible_from_root = False
    results_view = None

    members_order = [
        "survey",
        "title",
        "active"
    ]

    survey = schema.Reference(
        type = "woost.extensions.surveys.survey.Survey",
        bidirectional = True
    )

    title = schema.String(
        translated = True,
        required = True,
        descriptive = True
    )

    active = schema.Boolean(
        required = True,
        default = True
    )

    def init_survey_schema(self, survey_schema):
        raise TypeError(
            "%s doesn't implement the init_survey_schema() method"
            % self
        )

    def create_survey_field(self, member_type, **member_kwargs):

        if "name" not in member_kwargs:
            member_kwargs["name"] = "question%d" % self.id

        if "translate_value" not in member_kwargs:
            member_kwargs["__translate__"] = (
                lambda language, **kwargs: translations(self, **kwargs)
            )

        return member_type(**member_kwargs)

    def create_results_view(self):
        if self.results_view:
            view = templates.new(self.results_view)
            view.question = self
            return view


class SurveyOptionsQuestion(SurveyQuestion):

    results_view = "woost.extensions.surveys.SurveyOptionsQuestionResultsView"

    options = schema.Collection(
        items = "woost.extensions.surveys.survey.SurveyOption",
        bidirectional = True,
        integral = True,
        min = 1
    )

    def init_survey_schema(self, survey_schema):
        survey_schema.add_member(
            self.create_survey_field(
                schema.Reference,
                type = SurveyOption,
                required = True,
                enumeration = [
                    option
                    for option in self.options
                    if option.active
                ],
                edit_control = "cocktail.html.RadioSelector"
            ),
            append = True
        )


class SurveyOption(Item):

    visible_from_root = False

    members_order = [
        "question",
        "title",
        "active"
    ]

    question = schema.Reference(
        type = "woost.extensions.surveys.survey.SurveyOptionsQuestion",
        bidirectional = True
    )

    title = schema.String(
        translated = True,
        required = True,
        descriptive = True
    )

    active = schema.Boolean(
        required = True,
        default = True
    )


class SurveyTextQuestion(SurveyQuestion):

    mandatory = schema.Boolean(
        required = True,
        default = True
    )

    def init_survey_schema(self, survey_schema):
        survey_schema.add_member(
            self.create_survey_field(
                schema.String,
                required = self.mandatory,
                edit_control = "cocktail.html.TextArea"
            ),
            append = True
        )

