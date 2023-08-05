#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import mimetypes
from cStringIO import StringIO
import cherrypy
from cocktail.translations import translations
from cocktail.schema.io import export_file
from cocktail.controllers import request_property
from woost.controllers.backoffice.useractions import get_user_action
from woost.controllers.backoffice.editcontroller import EditController


class SurveyResultsController(EditController):

    view_class = "woost.extensions.surveys.SurveyResultsView"

    allowed_rendering_formats = (
        EditController.allowed_rendering_formats
        | frozenset(["msexcel"])
    )

    @cherrypy.expose
    def render_msexcel(self):

        survey = self.edit_node.item
        survey_schema = survey.create_survey_schema()

        mime_type = mimetypes.types_map[".xls"]
        cherrypy.response.headers['Content-Type'] = mime_type
        cherrypy.response.headers["Content-Disposition"] = \
            'attachment; filename="%s"' % (translations(survey) + ".xls")

        buffer = StringIO()
        export_file(
            survey.submissions,
            buffer,
            survey_schema,
            mime_type = mime_type
        )
        return buffer.getvalue()

    @request_property
    def output(self):
        output = EditController.output(self)
        output["selected_action"] = get_user_action("survey_results")
        return output

