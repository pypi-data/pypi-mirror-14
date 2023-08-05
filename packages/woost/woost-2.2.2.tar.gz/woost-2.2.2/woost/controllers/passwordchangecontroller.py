#-*- coding: utf-8 -*-
u"""Defines the `PasswordChangeController` class.

.. moduleauthor:: Javier Marrero <javier.marrero@whads.com>
"""
import hashlib
import cherrypy
from cocktail import schema
from cocktail.schema.exceptions import ValidationError
from cocktail.controllers import (
    request_property,
    FormProcessor,
    Form,
    Controller
)
from woost.models.emailtemplate import EmailTemplate
from woost.models import Configuration, User, Publishable
from woost.controllers.documentcontroller import DocumentController


class UserIdentifierNotRegisteredError(ValidationError):
    pass


class UserEmailMissingError(ValidationError):
    pass


def generate_confirmation_hash(identifier):
    hash = hashlib.sha1()
    hash.update(identifier)
    hash.update(Configuration.instance.secret_key)
    return hash.hexdigest()


class PasswordChangeController(FormProcessor, DocumentController):

    class_view = "woost.views.PasswordChangeRequestTemplate"

    class RequestPasswordChangeForm(Form):

        @request_property
        def schema(self):

            user_id_member = self.identifier_member.copy()
            user_id_member.name = "user"

            @user_id_member.add_validation
            def validate_user_identifier_exists(member, value, context):
                if value and self.user is None:
                    yield UserIdentifierNotRegisteredError(member, value, context)

            @user_id_member.add_validation
            def validate_user_has_email(member, value, context):
                if self.user is not None and not self.user.email:
                    yield UserEmailMissingError(member, value, context)

            return schema.Schema("PasswordChangeRequestForm", members = [
                user_id_member
            ])

        @request_property
        def identifier_member(self):
            cms = self.controller.context["cms"]
            return cms.authentication.identifier_field

        @request_property
        def identifier(self):
            return self.data["user"]

        @request_property
        def user(self):
            if self.identifier:
                return User.get_instance(**{
                    self.identifier_member.name: self.identifier
                })

        def after_submit(self):
            confirmation_email_template = EmailTemplate.get_instance(
                qname = "woost.password_change_email_template"
            )
            if confirmation_email_template:
                confirmation_email_template.send({
                    "user": self.user,
                    "confirmation_url": self.confirmation_url
                })

        @request_property
        def confirmation_url(self):
            confirmation_page = Publishable.require_instance(
                qname = 'woost.password_change_confirmation_page'
            )
            return confirmation_page.get_uri(
                host = ".",
                parameters = {
                    "user": self.identifier,
                    "hash": generate_confirmation_hash(self.identifier)
                }
            )

class PasswordChangeBlockController(Controller):

    @request_property
    def output(self):
        output = Controller.output(self)
        output["forms"] = cherrypy.request.handler_chain[-1].forms
        return output


class PasswordChangeConfirmationBlockController(Controller):

    @request_property
    def output(self):
        output = Controller.output(self)
        controller_output = cherrypy.request.handler_chain[-1].output
        for key in ("identifier", "hash", "forms"):
            output[key] = controller_output[key]
        return output

