#-*- coding: utf-8 -*-
"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
import cherrypy
from cocktail import schema
from cocktail.controllers import (
    Controller,
    FormProcessor,
    Form,
    request_property,
    context
)
from cocktail.controllers.location import Location
from woost import app
from woost.models import Item
from woost.controllers.backoffice.usereditnode import PasswordConfirmationError
from woost.extensions.signup.signupconfirmationcontroller import generate_confirmation_hash


class SignUpController(FormProcessor, Controller):

    is_transactional = True

    class SignUpForm(Form):

        @request_property
        def model(self):
            return self.controller.block.user_type

        @request_property
        def adapter(self):
            adapter = Form.adapter(self)
            adapter.implicit_copy = False
            adapter.copy(("email", "password"))
            return adapter

        @request_property
        def schema(self):
            adapted_schema = Form.schema(self)

            # Set schema name in order to keep always the same value
            # although change value of form_model member
            adapted_schema.name = u"SignUpForm"

            # Adding extra field for password confirmation
            if adapted_schema.get_member("password"):

                password_confirmation_member = schema.String(
                    name = "password_confirmation",
                    edit_control = "cocktail.html.PasswordBox",
                    required = adapted_schema.get_member("password"),
                    after_member = "password"
                )
                adapted_schema.add_member(password_confirmation_member)

                # Add validation to compare password_confirmation and
                # password fields
                @password_confirmation_member.add_validation
                def validate_password_confirmation(context):
                    password = context.get_value("password")
                    password_confirmation = context.value

                    if password and password_confirmation \
                    and password != password_confirmation:
                        yield PasswordConfirmationError(context)

            return adapted_schema

        def submit(self):
            Form.submit(self)
            block = self.controller.block

            # Adding roles
            for role in block.roles:
                if role not in self.instance.roles:
                    self.instance.roles.append(role)

            # If require email confirmation, disabled authenticated access
            confirmation_email_template = block.confirmation_email_template
            if confirmation_email_template:
                self.instance.enabled = False
                self.instance.confirmed_email = False
            else:
                self.instance.enabled = True

            self.instance.insert()

        def after_submit(self):
            block = self.controller.block

            # If require email confirmation send email confirmation message
            confirmation_email_template = block.confirmation_email_template
            if confirmation_email_template:
                confirmation_email_template.send(self.email_parameters)
                success_page = block.pending_page
            else:
                success_page = block.confirmation_page
                # Autologin
                app.authentication.set_user_session(self.instance)

            # Redirecting to the success page
            raise cherrypy.HTTPRedirect(success_page.get_uri())

        @request_property
        def email_parameters(self):
            parameters = {
                "user": self.instance,
                "confirmation_url": self.confirmation_url
            }
            return parameters

        @request_property
        def confirmation_url(self):
            uri = self.controller.block.confirmation_page.get_uri()
            location = Location.get_current(relative=False)
            location.path_info = uri
            location.query_string = {
                "email": self.instance.email,
                "hash": generate_confirmation_hash(self.instance.email)
            }
            return str(location)
