#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
from cocktail.html import Element
from cocktail.translations import translations
from cocktail.controllers import context
from woost.views.itemlabel import ItemLabel


class ContentLink(ItemLabel):

    referer = None
    icon_visible = False

    def __init__(self, item = None, referer = None, **kwargs):
        Element.__init__(self, **kwargs)
        self.item = item
        self.referer = referer

    def _ready(self):

        ItemLabel._ready(self)

        if self.item:
            self.tag = "a"
            self["href"] = self.get_edit_url()
        else:
            self.append(u"-")

    def get_edit_url(self):
        return context["cms"].contextual_uri(
            "content", self.item.id, "fields"
        )

