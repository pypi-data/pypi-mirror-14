#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension, extension_translations

translations.define("FormsExtension",
    ca = u"Formularis personalitzats",
    es = u"Formularios personalizados",
    en = u"Custom forms"
)

translations.define("FormsExtension-plural",
    ca = u"Formularis personalitzats",
    es = u"Formularios personalizados",
    en = u"Custom forms"
)


class FormsExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet dissenyar formularis des del gestor.""",
            "ca"
        )
        self.set("description",
            u"""Permite diseñar formularios des del gestor.""",
            "es"
        )
        self.set("description",
            u"""Design forms directly from the backoffice.""",
            "en"
        )

    def _load(self):

        from woost.extensions.forms import (
            strings,
            formblock,
            formagreement,
            fields,
            typegroups,
            exportformdataaction
        )

        from woost.controllers.backoffice.backofficecontroller \
            import BackOfficeController

        from woost.extensions.forms.exportformdatacontroller \
            import ExportFormDataController

        BackOfficeController.export_form_data = ExportFormDataController

    def _install(self):
        self.create_default_email_notification()

    def create_default_email_notification(self):

        from woost.models import EmailTemplate, Configuration
        from woost.extensions.forms import installationstrings

        try:
            default_host = Configuration.instance.websites[0].hosts[0]
        except:
            sender = None
        else:
            pos = default_host.find(":")
            if pos != -1:
                default_host = default_host[:pos]
            parts = default_host.split(".")
            if len(parts) > 2:
                default_host = ".".join(parts[-2:])
            sender = "'info@%s'" % default_host

        email = self._create_asset(
            EmailTemplate,
            "default_email_notification",
            title = extension_translations,
            sender = sender,
            receivers = "notification_receivers",
            template_engine = "mako",
            subject = extension_translations,
            body = extension_translations,
            initialization_code =
                "from cocktail.stringutils import decapitalize\n"
                "from cocktail.translations import translations\n"
                "from cocktail.html import templates\n"
                "form_description = decapitalize(translations(block))\n"
                "table = templates.new('cocktail.html.EmailPropertyTable')\n"
                "table.schema = form_schema\n"
                "table.data = form_data\n"
                "form_contents = table.render()",
            condition = "should_send = bool(notification_receivers)"
        )

