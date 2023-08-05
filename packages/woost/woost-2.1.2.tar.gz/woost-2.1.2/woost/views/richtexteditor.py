#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
from cocktail.html import templates
from cocktail.translations import translations
from woost.models import Style

TinyMCE = templates.get_class("cocktail.html.TinyMCE")


class RichTextEditor(TinyMCE):

    styles = None
    tinymce_params = {
        "setup": "woost.richTextEditor.init",
        "plugins": "table link image fullscreen code "
                   "visualblocks contextmenu paste",
        "entity_encoding": "raw",
        "style_formats_merge": True,
        "height": 250,
        "content_css": "/user_styles/?backoffice=1",
        "statusbar": False,
        "menubar": [
            "edit",
            "insert",
            "table",
            "view"
        ],
        "menu": {
            "edit": {
                "title": "Edit",
                "items": "undo redo | "
                "cut copy paste pastetext | "
                "selectall | "
                "removeformat"
            },
            "insert": {
                "title": "Insert",
                "items": "image link"
            },
            "table": {
                "title": "Table",
                "items": "inserttable tableprops deletetable | cell row column"
            },
            "view": {
                "title": "View",
                "items": "visualaid visualblocks code fullscreen"
            }
        },
        "toolbar": "undo redo | "
                   "styleselect | "
                   "bold italic | "
                   "bullist numlist outdent indent"
    }

    def _build(self):
        TinyMCE._build(self)
        self.add_resource("/resources/scripts/RichTextEditor.js")

    def _get_default_styles(self):
        return list(Style.select({"applicable_to_text": True}))

    def _ready(self):

        styles = self.styles
        if styles is None:
            styles = self._get_default_styles()

        if styles:
            self.tinymce_params.setdefault("style_formats", [{
                "title": translations(
                    "woost.views.RichTextEditor.styles_menu_entry"
                ),
                "items": [
                    {
                        "title": translations(style),
                        "inline": "span",
                        "classes": style.class_name
                    }
                    for style in styles
                ]
            }])

        TinyMCE._ready(self)

