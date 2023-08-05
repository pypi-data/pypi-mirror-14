#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from .block import Block


class HTMLBlock(Block):

    instantiable = True
    type_group = "blocks.custom"
    view_class = "cocktail.html.Element"

    html = schema.CodeBlock(
        language = "html",
        member_group = "content"
    )

    translated_html = schema.CodeBlock(
        translated = True,
        language = "html",
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        html = self.translated_html or self.html
        if html:
            view.append(html)

