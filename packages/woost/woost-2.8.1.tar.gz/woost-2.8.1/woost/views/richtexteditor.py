#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
from cocktail.html import templates
from cocktail.html.utils import is_inline_element
from cocktail.translations import translations
from woost.models import Style

TinyMCE = templates.get_class("cocktail.html.TinyMCE")


class RichTextEditor(TinyMCE):

    styles = None
    shortcuts = None

    tinymce_params = {
        "setup": "woost.richTextEditor.init",
        "plugins": "table link image fullscreen code "
                   "visualblocks contextmenu paste",
        "entity_encoding": "raw",
        "style_formats_merge": True,
        "height": 250,
        "content_css": "/user_styles/?backoffice=1",
        "convert_urls": False,
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

    def __init__(self, *args, **kwargs):
        TinyMCE.__init__(self, *args, **kwargs)
        self.shortcuts = list(self.shortcuts) if self.shortcuts else []

    def _build(self):
        TinyMCE._build(self)
        self.add_resource("/resources/scripts/RichTextEditor.js")

    def _get_default_styles(self):
        return list(Style.select({"applicable_to_text": True}))

    def _get_tinymce_style_definition(self, style):
        style_dfn = self._get_tinymce_format_definition(style)
        style_dfn["title"] = translations(style)
        return style_dfn

    def _get_tinymce_format_definition(self, style):

        format_dfn = {
            "inline": "span",
            "classes": style.class_name
        }

        if style.html_tag:
            if is_inline_element(style.html_tag):
                format_dfn["inline"] = style.html_tag
            else:
                format_dfn["block"] = style.html_tag

        return format_dfn

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
                    self._get_tinymce_style_definition(style)
                    for style in styles
                ]
            }])

            shortcuts = list(self.shortcuts)
            formats = {}

            for style in styles:
                if style.editor_keyboard_shortcut:
                    format_id = style.class_name
                    formats[format_id] = \
                        self._get_tinymce_format_definition(style)
                    shortcuts.append([
                        style.editor_keyboard_shortcut,
                        translations(style),
                        "this.formatter.apply('%s');" % format_id
                    ])

            if formats:
                self.tinymce_params.setdefault("formats", formats)

            if shortcuts:
                self.tinymce_params["woostShortcuts"] = shortcuts

        TinyMCE._ready(self)

