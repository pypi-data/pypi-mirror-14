#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cStringIO import StringIO
import mimetypes
import cherrypy
from cocktail.translations import translations
from cocktail import schema
from cocktail.schema.io import export_msexcel
from cocktail.controllers import request_property, get_parameter
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from .formblock import FormBlock


class ExportFormDataController(BaseBackOfficeController):

    @request_property
    def form(self):
        return get_parameter(
            schema.Reference("form", type = FormBlock, required = True),
            errors = "raise"
        )

    def __call__(self, *args, **kwargs):

        form = self.form
        form_model = form.field_set.create_form_model()

        cherrypy.response.headers['Content-Type'] = \
            mimetypes.types_map.get(".xls")

        cherrypy.response.headers["Content-Disposition"] = \
            'attachment; filename="%s.xls"' % translations(form)

        buffer = StringIO()
        export_msexcel(
            form.submitted_data,
            buffer,
            form_model,
            form_model.ordered_members()
        )
        return buffer.getvalue()

