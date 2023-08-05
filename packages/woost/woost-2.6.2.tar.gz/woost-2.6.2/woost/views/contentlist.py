#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
from cocktail.html import templates
from cocktail.html.uigeneration import UIGenerator
from woost.models import get_current_user, ReadPermission
from woost.views.uigeneration import backoffice_display

List = templates.get_class("cocktail.html.List")


class ContentList(List, UIGenerator):

    referer = None
    base_ui_generators = [backoffice_display]

    def __init__(self, *args, **kwargs):
        List.__init__(self, *args, **kwargs)
        UIGenerator.__init__(self)

    def _fill_entries(self):

        user = get_current_user()
        items = self.items

        if items is not None:
            items = [
                item
                for item in self.items
                if user.has_permission(ReadPermission, target = item)
            ]

        if items:
            List._fill_entries(self)
        else:
            self.tag = "div"
            self.append(u"-")

    def create_entry_content(self, item):

        if self.member is not None and self.member.items is not None:
            display = self.create_member_display(
                None,
                self.member.items,
                item,
                referer = self.referer or self.data
            )
        else:
            display = self.create_object_display(
                item,
                referer = self.referer or self.data
            )

        if (
            self.referer
            and self.member
            and getattr(display, "item_label", None)
        ):
            display.item_label["data-woost-relativedrop"] = "%d.%s.%d" % (
                self.referer.id,
                self.member.name,
                item.id
            )

        return display

