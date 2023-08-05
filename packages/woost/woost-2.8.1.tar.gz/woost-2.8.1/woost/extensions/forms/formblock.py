#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import extend
from cocktail import schema
from cocktail.translations import translations
from cocktail.persistence import PersistentList
from cocktail.controllers import request_property
from woost.models import Block, EmailTemplate, Publishable
from .fields import FieldSet, Field, OptionsFieldOption


class FormBlock(Block):

    type_group = "blocks.forms"

    groups_order = list(Block.groups_order)
    groups_order.insert(1, "form")

    members_order = [
        "field_set",
        "agreements",
        "notification_receivers",
        "email_messages",
        "redirection",
        "submit_code",
        "after_submit_code",
        "view_class"
    ]

    default_controller = "woost.extensions.forms.formcontroller.FormController"

    field_set = schema.Reference(
        type = FieldSet,
        related_end = schema.Collection(),
        required = True,
        member_group = "form"
    )

    agreements = schema.Collection(
        items = "woost.extensions.forms.formagreement.FormAgreement",
        bidirectional = True,
        member_group = "form"
    )

    notification_receivers = schema.Collection(
        items = schema.EmailAddress(),
        member_group = "form"
    )

    email_messages = schema.Collection(
        items = schema.Reference(type = EmailTemplate),
        related_end = schema.Collection(),
        default = schema.DynamicDefault(
            lambda: filter(None, [
                EmailTemplate.get_instance(
                    qname = "woost.extensions.forms.default_email_notification"
                )
            ])
        ),
        member_group = "form"
    )

    redirection = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "form"
    )

    submit_code = schema.CodeBlock(
        language = "python",
        member_group = "administration"
    )

    after_submit_code = schema.CodeBlock(
        language = "python",
        member_group = "administration"
    )

    view_class = schema.String(
        shadows_attribute = True,
        after_member = "controller",
        listed_by_default = False,
        default = "woost.extensions.forms.FormView",
        member_group = "behavior"
    )

    def __init__(self, *args, **kwargs):
        Block.__init__(self, *args, **kwargs)
        self.submitted_data = PersistentList()

    def init_view(self, view):
        Block.init_view(self, view)
        view.depends_on(Field)
        view.depends_on(OptionsFieldOption)

    @request_property
    def form_model(self):
        return self.field_set.create_form_model()

