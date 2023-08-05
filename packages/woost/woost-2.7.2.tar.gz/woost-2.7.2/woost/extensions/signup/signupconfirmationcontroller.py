#-*- coding: utf-8 -*-
"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
import hashlib
import cherrypy
from cocktail import schema
from cocktail.persistence import transaction
from cocktail.controllers import request_property
from woost import app
from woost.models import User
from woost.controllers.documentcontroller import DocumentController
from woost.extensions.signup import SignUpExtension


def generate_confirmation_hash(email):
    hash = hashlib.sha1()
    hash.update(email)
    hash.update(SignUpExtension.instance.secret_key)
    return hash.hexdigest()


class SignUpConfirmationController(DocumentController):

    autologin = True

    def __init__(self, *args, **kwargs):
        self.email = self.params.read(schema.String("email"))
        self.hash = self.params.read(schema.String("hash"))

    def confirm_user(self, user):
        user.confirmed_email = True
        user.enabled = True

    def submit(self):

        if self.email or self.hash:
            # Checking hash code
            if generate_confirmation_hash(self.email) == self.hash:
                instance = User.get_instance(email=self.email)
                if instance:
                    # Confirming and enabling user instance
                    transaction(self.confirm_user, action_args = [instance])

                    # Autologin after confirmation
                    if self.autologin:
                        app.authentication.set_user_session(instance)

                    raise cherrypy.HTTPRedirect(app.publishable.get_uri())

            raise cherrypy.HTTPError(400, "Invalid hash")

