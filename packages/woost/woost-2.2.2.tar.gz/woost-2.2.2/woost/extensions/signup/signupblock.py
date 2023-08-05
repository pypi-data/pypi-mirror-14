#-*- coding: utf-8 -*-
"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
from cocktail import schema
from woost.models import (
    Block,
    EmailTemplate,
    Publishable,
    Role,
    User
)

def excluded_roles():
    return Role.qname.not_one_of((
        'woost.anonymous',
        'woost.everybody',
        'woost.authenticated'
    ))

class SignUpBlock(Block):

    type_group = "blocks.forms"
    view_class = "woost.extensions.signup.SignUpForm"

    members_order = [
        "user_type",
        "roles",
        "confirmation_email_template",
        "confirmation_page",
        "pending_page"
    ]

    # Defines the persistent class that will be
    # used like schema in signup process
    user_type = schema.Reference(
        class_family = User,
        required = True,
        member_group = "signup_process"
    )

    # The collection of roles that will be applyed
    # to each instance (of user_type class) created throw
    # a signuppage
    roles = schema.Collection(
        items = schema.Reference(type = Role),
        relation_constraints = lambda ctx: [excluded_roles()],
        related_end = schema.Collection(),
        member_group = "signup_process",
        listed_by_default = False,
    )

    # If is None, doesn't require an email confirmation
    # process to complete signup process
    confirmation_email_template = schema.Reference(
        type = EmailTemplate,
        related_end = schema.Collection(),
        default = schema.DynamicDefault(
            lambda: EmailTemplate.get_instance(
                qname = u"woost.extensions.signup.signup_confirmation_email_template"
            )
        ),
        member_group = "signup_process"
    )

    confirmation_page = schema.Reference(
        type = Publishable,
        required = True,
        related_end = schema.Collection(),
        default = schema.DynamicDefault(
            lambda: Publishable.get_instance(
                qname = u"woost.extensions.signup.signup_confirmation_page"
            )
        ),
        member_group = "signup_process"
    )

    pending_page = schema.Reference(
        type = Publishable,
        exclusive = lambda ctx:
            ctx.validable.get("confirmation_email_template"),
        related_end = schema.Collection(),
        default = schema.DynamicDefault(
            lambda: Publishable.get_instance(
                qname = u"woost.extensions.signup.signup_pending_page"
            )
        ),
        member_group = "signup_process"
    )

