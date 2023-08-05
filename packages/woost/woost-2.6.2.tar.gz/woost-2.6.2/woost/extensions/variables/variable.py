#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models import Item


class Variable(Item):

    members_order = [
        "identifier",
        "text",
        "translated_text"
    ]

    identifier = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = False,
        descriptive = True
    )

    text = schema.String(
        edit_control = "cocktail.html.TextArea"
    )

    translated_text = schema.String(
        translated = True,
        edit_control = "cocktail.html.TextArea"
    )

    expression = schema.CodeBlock(
        language = "python"
    )

    def get_value(self):

        text = self.translated_text or self.text

        expr = self.expression
        if expr:
            code_object = compile(
                self.expression,
                "%r.expression" % self,
                "exec"
            )
            context = {"self": self, "text": text}
            exec code_object in context
            text = context["text"]

        return text

