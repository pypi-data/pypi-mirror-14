#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail.controllers import (
    Controller,
    FormProcessor,
    Form,
    request_property
)


class SurveyController(FormProcessor, Controller):

    is_transactional = True

    class SurveyForm(Form):

        @request_property
        def survey(self):
            return self.controller.block.survey

        @request_property
        def schema(self):
            return self.survey.create_survey_schema()

        def submit(self):
            Form.submit(self)
            self.survey.add_submission(self.data)

        def after_submit(self):
            if self.controller.block.redirection:
                raise cherrypy.HTTPRedirect(
                    self.controller.block.redirection.get_uri()
                )
            else:
                self.controller.context["publishable"].first_child_redirection()

