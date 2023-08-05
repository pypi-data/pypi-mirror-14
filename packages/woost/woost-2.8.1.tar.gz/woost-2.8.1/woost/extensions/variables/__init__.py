#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import re
from cocktail.translations import translations
from woost.models import Extension

translations.define("VariablesExtension",
    ca = u"Variables",
    es = u"Variables",
    en = u"Variables"
)

translations.define("StaticPubExtension-plural",
    ca = u"Variables",
    es = u"Variables",
    en = u"Variables"
)

variable_regex = re.compile("{{([a-z0-9A-Z.-_]+)}}")


class VariablesExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Permet aplicar patrons de substitució de text.""",
            "ca"
        )
        self.set("description",
            u"""Permite aplicar patrones de sustitución de texto.""",
            "es"
        )
        self.set("description",
            u"""Replace text patterns with centrally defined variables.""",
            "en"
        )

    def _load(self):

        from woost.extensions.variables import (
            strings,
            variable,
            migration
        )

        from woost.controllers.publishablecontroller \
            import PublishableController

        base_produce_content = PublishableController._produce_content

        def produce_content_with_variable_replacement(controller, **kwargs):
            content = base_produce_content(controller, **kwargs)
            content = self.replace_variables(content)
            return content

        PublishableController._produce_content = \
            produce_content_with_variable_replacement

    def replace_variables(self, content):
        return variable_regex.sub(self.__replacement, content)

    def __replacement(self, match):
        from woost.extensions.variables.variable import Variable
        variable = Variable.require_instance(identifier = match.group(1))
        return variable.get_value()

