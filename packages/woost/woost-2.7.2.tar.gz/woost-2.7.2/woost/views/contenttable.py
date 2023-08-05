#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
"""
from cocktail.pkgutils import resolve
from cocktail.translations import translations
from cocktail.schema import RelationMember
from cocktail.schema.expressions import (
    PositiveExpression,
    NegativeExpression
)
from cocktail.html import Element, templates
from cocktail.html.uigeneration import UIGenerator
from cocktail.controllers import view_state
from cocktail.controllers.userfilter import user_filters_registry
from woost.models import Item
from woost.views.uigeneration import backoffice_display
from woost.controllers.backoffice.useractions import export_user_actions

Table = templates.get_class("cocktail.html.Table")
ItemContextMenu = templates.get_class("woost.views.ItemContextMenu")


class ContentTable(Table):

    base_url = None
    entry_selector = "tbody tr.item_row"
    base_ui_generators = [backoffice_display]
    use_separate_selection_column = False
    action_context = None

    def __init__(self, *args, **kwargs):
        Table.__init__(self, *args, **kwargs)
        self.set_member_expression("class", lambda obj: obj.__class__)
        self.set_member_sortable("class", False)
        self.set_member_expression("element", lambda obj: obj)
        self.set_member_sortable("element", False)
        self.set_member_expression("thumbnail", lambda obj: obj)
        self.set_member_sortable("thumbnail", False)

    def _fill_head(self):
        Table._fill_head(self)
        if self.head_row.children:
            self.head_row.children[-1].add_class("last")

    def create_row(self, index, item):
        row = Table.create_row(self, index, item)
        row.add_class("item_row")

        # Indicate to the client which actions are available on each item
        if self.action_context:
            export_user_actions(row, self.action_context, item)

        row.context_menu = self.create_row_context_menu(item)
        row.children[0].append(row.context_menu)
        return row

    def create_row_context_menu(self, item):
        menu = ItemContextMenu()
        menu.item = item
        menu.menu_owner_selector = "tr"
        menu.effect_on_selection = "change"
        return menu

    def create_cell(self, item, column, language = None):
        cell = Table.create_cell(self, item, column, language = language)

        # Drag & drop information
        if isinstance(column, RelationMember):
            cell["data-woost-drop"] = "%d.%s" % (item.id, column.name)

        return cell

    def add_header_ui(self, header, column, language):

        # Add visual cues for sorted columns
        sortable = self.get_member_sortable(column)

        if sortable and self.order:
            current_direction = self._sorted_columns.get(
                (column.name, language)
            )

            if current_direction is not None:

                header.add_class("sorted")

                if current_direction is PositiveExpression:
                    header.add_class("ascending")
                    sign = "-"
                elif current_direction is NegativeExpression:
                    header.add_class("descending")

        # Column options
        if sortable or self.get_member_searchable(column):

            menu = header.menu = templates.new("cocktail.html.DropdownPanel")
            menu.add_class("column_dropdown")
            header.append(menu)

            menu.label.append(header.label)

            if column.translated:
                menu.label.append(header.translation_label)

            options = header.menu.options = self.create_column_panel(
                column,
                language
            )
            menu.panel.append(options)

    def create_column_panel(self, column, language):

        options = Element()
        options.add_class("column_panel")

        if self.get_member_sortable(column):
            sorting_options = self.create_sorting_options(column, language)
            options.append(sorting_options)

            if column.grouping:
                grouping_options = self.create_grouping_options(
                    column,
                    language
                )
                options.append(grouping_options)

        if self.get_member_searchable(column):
            search_options = self.create_search_options(column, language)
            options.append(search_options)

        return options

    def create_sorting_options(self, column, language):

        if self.order:
            direction = self._sorted_columns.get((column.name, language))
        else:
            direction = None

        order_param = column.name
        if language:
            order_param += "." + language

        options = Element()
        options.add_class("sorting_options")

        title = Element("div")
        title.add_class("options_header")
        title.append(translations("woost.views.ContentTable sorting header"))
        options.append(title)

        asc = options.ascending = Element("a")
        asc.add_class("ascending")
        asc["href"] = "?" + view_state(order = order_param, page = 0)
        asc.append(translations("woost.views.ContentTable sort ascending"))
        options.append(asc)

        if direction is PositiveExpression:
            asc.add_class("selected")

        desc = options.ascending = Element("a")
        desc.add_class("descending")
        desc["href"] = "?" + view_state(order = "-" + order_param, page = 0)
        desc.append(translations("woost.views.ContentTable sort descending"))
        options.append(desc)

        if direction is NegativeExpression:
            desc.add_class("selected")

        return options

    def create_search_options(self, column, language):

        filters = (
            [filter.id for filter in self.filters]
            if self.filters
            else []
        )

        filter_state = user_filters_registry.get_new_filter_view_state(
            self.schema,
            filters,
            column
        )
        filter_state["page"] = "0"

        options = Element()
        options.add_class("search_options")

        title = Element("div")
        title.add_class("options_header")
        title.append(translations("woost.views.ContentTable search header"))
        options.append(title)

        add_filter = Element("a")
        add_filter.add_class("add_filter")
        add_filter["href"] = "?" + view_state(**filter_state)
        add_filter.append(
            translations("woost.views.ContentTable add column filter")
        )
        add_filter.set_client_param("filterId", "member-" + column.name)
        options.append(add_filter)

        return options

    def create_grouping_options(self, column, language):

        options = Element()
        options.add_class("grouping_options")

        title = Element("div")
        title.add_class("options_header")
        title.append(translations("woost.views.ContentTable grouping header"))
        options.append(title)

        grouping_class = resolve(column.grouping)
        variants = (None,) + grouping_class.variants

        table = Element("table")
        options.append(table)

        for variant in variants:

            tr = Element("tr")
            table.append(tr)

            td = Element("td")
            td.add_class("variant")
            td.append(grouping_class.translate_grouping_variant(variant))
            tr.append(td)

            for sign in (PositiveExpression, NegativeExpression):
                grouping = grouping_class()
                grouping.member = column
                grouping.language = language
                grouping.sign = sign
                grouping.variant = variant

                td = Element("td")
                td.add_class("sign")
                tr.append(td)

                grouping_link = Element("a")
                grouping_link.add_class("grouping")
                grouping_link["href"] = \
                    "?" + view_state(grouping = grouping.request_value, page = 0)
                grouping_link.append(
                    translations(
                        "cocktail.controllers.grouping.MemberGrouping-"
                        + ("ascending"
                            if sign is PositiveExpression
                            else "descending")
                    )
                )
                td.append(grouping_link)

        return options

