#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Javier Marrero <javier.marrero@whads.com>
"""
from copy import deepcopy
from cocktail.html import templates
RichTextEditor = templates.get_class("woost.views.RichTextEditor")


class NewsletterRichTextEditor(RichTextEditor):

    tinymce_params = deepcopy(RichTextEditor.tinymce_params)

    tinymce_params["plugins"] = " ".join(
        plugin
        for plugin in tinymce_params["plugins"].split()
        if plugin not in ("image", "table")
    )

    tinymce_params["menu"]["insert"]["items"] = " ".join(
        cmd
        for cmd in tinymce_params["menu"]["insert"]["items"].split()
        if cmd != "image"
    )

    tinymce_params["menu"].pop("table", None)

