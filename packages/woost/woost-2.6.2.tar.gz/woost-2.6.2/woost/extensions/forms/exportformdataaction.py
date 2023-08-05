#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.controllers.backoffice.useractions import UserAction
from .formblock import FormBlock


class ExportFormDataAction(UserAction):

    content_type = FormBlock
    included = frozenset(["item_buttons", "block_menu"])
    min = 1
    max = 1
    icon_uri = "/resources/images/export_xls.png"

    def get_url(self, controller, selection):
        return controller.contextual_uri(
            self.id,
            form = selection[0].id
        )


ExportFormDataAction("export_form_data").register()

