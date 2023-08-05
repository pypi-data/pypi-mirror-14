#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
"""
from cocktail.schema import Collection, Reference
from cocktail.translations import translations
from cocktail.html import Element, templates
from woost.views.uigeneration import backoffice_edit_control

Form = templates.get_class("cocktail.html.Form")


class ContentForm(Form):

    table_layout = False
    redundant_translation_labels = False
    base_ui_generators = [backoffice_edit_control]
    referer = None

    def create_member_display(self, obj, member, value, **context):
        context.setdefault("referer", self.persistent_object)
        return Form.create_member_display(self, obj, member, value, **context)

    def create_fieldset(self, group):
        fieldset = Form.create_fieldset(self, group)
        fieldset.set_client_param("group", group)
        return fieldset

    def get_group_label(self, group):

        label = Form.get_group_label(self, group)

        if not label and (not group or group == "default"):
            label = translations(self.schema.original_member.name)

        return label

