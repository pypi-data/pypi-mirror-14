#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.controllers import request_property
from woost.controllers.backoffice.useractions import get_user_action
from woost.controllers.backoffice.editcontroller import EditController


class ReferencesController(EditController):

    view_class = "woost.views.BackOfficeReferencesView"

    @request_property
    def references(self):
        return get_user_action("references").references

    @request_property
    def output(self):
        output = EditController.output(self)
        output.update(
            selected_action = get_user_action("references"),
            references = self.references
        )
        return output

