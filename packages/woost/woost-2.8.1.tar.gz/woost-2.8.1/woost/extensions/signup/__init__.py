#-*- coding: utf-8 -*-
"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""

import random
import string
from cocktail import schema
from cocktail.translations import translations
from woost.models import Extension

translations.define("SignUpExtension",
    ca = u"Alta d'usuaris",
    es = u"Alta de usuarios",
    en = u"Sign Up"
)

translations.define("SignUpExtension-plural",
    ca = u"Altas d'usuaris",
    es = u"Altas de usuarios",
    en = u"Signs Up"
)

class SignUpExtension(Extension):

    # To indicate if the extension was loaded at least one time
    # will be set to True at the end of the first load
    initialized = False

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet als usuaris registrar-se autònomament en el lloc web""",
            "ca"
        )
        self.set("description",
            u"""Permite a los usuarios registrarse por si mismos en el sitio""",
            "es"
        )
        self.set("description",
            u"""Allows users to register themselves on the site""",
            "en"
        )
        self.secret_key = self._generate_secret_key()

    def _generate_secret_key(self):
        secret_key = ''
        for i in range(0,8):
            secret_key = secret_key + \
                random.choice(
                    string.letters + string.digits
                )
        return secret_key

    def _load(self):

        from woost.extensions.signup import (
            signupblock,
            user,
            strings
        )

        self.install()

    def _install(self):

        from woost.models import (
            extension_translations,
            Configuration,
            User,
            Controller,
            Document,
            Page,
            EmailTemplate,
            TextBlock
        )
        from woost.extensions.signup.signupblock import SignUpBlock

        signup_confirmation_controller = self._create_asset(
            Controller,
            "signup_confirmation_controller",
            python_name =
                "woost.extensions.signup.signupconfirmationcontroller."
                "SignUpConfirmationController",
            title = extension_translations
        )

        confirmation_email_template = self._create_asset(
            EmailTemplate,
            "signup_confirmation_email_template",
            template_engine = u"mako",
            sender = "'%s'" % User.require_instance(qname="woost.administrator").email,
            receivers = u"[user.email]",
            title = extension_translations,
            subject = extension_translations,
            body = extension_translations
        )

        pending_page = self._create_asset(
            Page,
            "signup_pending_page",
            title = extension_translations,
            hidden = True,
            blocks = [
                self._create_asset(
                    TextBlock,
                    "signup_pending_text_block",
                    text = extension_translations
                )
            ]
        )

        confirmation_page = self._create_asset(
            Page,
            "signup_confirmation_page",
            title = extension_translations,
            controller = signup_confirmation_controller,
            hidden = True,
            blocks = [
                self._create_asset(
                    TextBlock,
                    "signup_confirmation_text_block",
                    text = extension_translations
                )
            ]
        )

        signup_page = self._create_asset(
            Page,
            "signup_page",
            title = extension_translations,
            parent = Configuration.instance.websites[0].home,
            hidden = True,
            blocks = [
                self._create_asset(
                    SignUpBlock,
                    "signup_block",
                    user_type = User,
                    confirmation_email_template = confirmation_email_template,
                    confirmation_page = confirmation_page,
                    pending_page = pending_page,
                    controller = "woost.extensions.signup.signupcontroller.SignUpController"
                )
            ]
        )

        signup_page.children.append(pending_page, confirmation_page)

