#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.controllers import (
    request_property,
    get_parameter,
    Pagination
)
from .block import Block
from .elementtype import ElementType
from .news import News


class NewsListing(Block):

    max_page_size = 50

    instantiable = True
    type_group = "blocks.listings"

    groups_order = list(Block.groups_order)
    groups_order.insert(groups_order.index("content") + 1, "listing")

    members_order = [
        "element_type",
        "paginated",
        "page_size",
        "view_class"
    ]

    element_type = ElementType(
        member_group = "content"
    )

    paginated = schema.Boolean(
        required = True,
        default = False,
        member_group = "listing"
    )

    page_size = schema.Integer(
        min = 1,
        required = paginated,
        member_group = "listing"
    )

    view_class = schema.String(
        required = True,
        shadows_attribute = True,
        enumeration = [
            "woost.views.CompactNewsListing",
            "woost.views.TextOnlyNewsListing",
            "woost.views.TextAndImageNewsListing"
        ],
        default = "woost.views.TextOnlyNewsListing",
        member_group = "listing"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        view.tag = self.element_type
        view.name_prefix = self.name_prefix
        view.name_suffix = self.name_suffix
        view.depends_on(News)

        if self.paginated:
            view.pagination = self.pagination
        else:
            view.news = self.select_news()

    def select_news(self):
        news = News.select_accessible(order = "-news_date")

        if not self.paginated and self.page_size:
            news.range = (0, self.page_size)

        return news

    @request_property
    def pagination(self):
        return get_parameter(
            self.pagination_member,
            errors = "set_default",
            prefix = self.name_prefix,
            suffix = self.name_suffix
        )

    @request_property
    def pagination_member(self):
        return Pagination.copy(**{
            "page_size.default": self.page_size,
            "page_size.max": self.max_page_size,
            "items": self.select_news()
        })

