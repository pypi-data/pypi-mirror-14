#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.html import templates
from cocktail.html.uigeneration import display_factory
from woost.models import Item

ContentList = templates.get_class("woost.views.ContentList")


class ImageCollectionDisplay(ContentList):

    icon_factory = "backoffice_small_thumbnail.png"

    def __init__(self, *args, **kwargs):
        ContentList.__init__(self, *args, **kwargs)

        def thumbnail(ui_generator, obj, member, value, **context):
            display = templates.new("woost.views.ItemDisplay")
            display.label_visible = False
            display.icon_visible = True
            display.icon_factory = self.icon_factory
            return display

        self.set_member_type_display(Item, thumbnail)

    def create_member_display(self, *args, **kwargs):
        return ContentList.create_member_display(self, *args, **kwargs)

