#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2013
"""
from cocktail.modeling import cached_getter
from cocktail import schema
from woost.models import User
from woost.controllers.backoffice.editstack import EditNode


class SiteInstallationEditNode(EditNode):

    @cached_getter
    def form_adapter(self):

        form_adapter = EditNode.form_adapter(self)

        if self.item.is_inserted:
            form_adapter.exclude("change_password")

            if User.encryption_method:
                kwargs = {
                    "export_condition": False,
                    "import_condition": lambda context:
                        context.get("change_password", default = None)
                }
            else:
                kwargs = {}

            form_adapter.copy("synchronization_password", **kwargs)

        return form_adapter

    @cached_getter
    def form_schema(self):

        form_schema = EditNode.form_schema(self)
        password_member = form_schema.get_member("synchronization_password")

        if password_member:

            if User.encryption_method:

                order = form_schema.members_order = list(form_schema.members_order)
                pos = order.index("synchronization_password")

                if self.item.is_inserted:

                    change_password_member = schema.Boolean(
                        name = "change_password",
                        required = True,
                        default = False,
                        visible_in_detail_view = False
                    )
                    form_schema.add_member(change_password_member)
                    order.insert(pos, "change_password")

                    password_member.exclusive = change_password_member

            # No encryption: edit passwords in plain sight
            else:
                password_member.edit_control = "cocktail.html.TextBox"

        return form_schema

    def iter_changes(self):

        # Discard differences in the password field
        for member, language in EditNode.iter_changes(self):
            if not User.encryption_method or member.name not in (
                "change_password", "synchronization_password"
            ):
                yield (member, language)

