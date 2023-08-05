#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			August 2009
"""
from cocktail.modeling import getter, cached_getter
from cocktail.schema.expressions import (
    Self,
    Constant,
    InclusionExpression,
    ExclusionExpression,
    IsInstanceExpression,
    IsNotInstanceExpression
)
from cocktail import schema
from cocktail.translations import translations
from cocktail.html import templates
from cocktail.html.datadisplay import MULTIPLE_SELECTION
from cocktail.controllers.userfilter import (
    UserFilter,
    CollectionFilter,
    user_filters_registry,
    DescendsFromFilter
)
from woost import app
from .item import Item
from .changesets import ChangeSet, ChangeSetHasChangeExpression
from .publishable import Publishable, IsPublishedExpression
from .document import Document


class IsPublishedFilter(UserFilter):

    id = "published"

    @cached_getter
    def schema(self):
        return schema.Schema()

    @cached_getter
    def expression(self):
        return IsPublishedExpression(app.user)

user_filters_registry.add(Publishable, IsPublishedFilter)


class TypeFilter(UserFilter):
    id = "type"
    operators = ["eq", "ne"]

    @cached_getter
    def schema(self):
        return schema.Schema("UserFilter", members = [
            schema.String(
                "operator",
                required = True,
                enumeration = self.operators
            ),
            schema.Collection(
                "types",
                items = schema.Reference("item_type",
                    class_family = self.content_type
                )
            ),
            schema.Boolean(
                "is_inherited"
            )
        ])

    @cached_getter
    def expression(self):

        if self.operator == "eq":
            return IsInstanceExpression(Self, tuple(self.types), self.is_inherited)
        elif self.operator == "ne":
            return IsNotInstanceExpression(Self, tuple(self.types), self.is_inherited)

user_filters_registry.add(Item, TypeFilter)

class ItemSelectorFilter(schema.Reference.user_filter):

    def search_control(self, parent, obj, member):
        control = templates.new("woost.views.ItemSelector")
        control.existing_items_only = True
        return control

schema.Reference.user_filter = ItemSelectorFilter

def _collection_search_control(self, parent, obj, member):
    control = templates.new("woost.views.ItemSelector")
    control.existing_items_only = True
    return control

CollectionFilter.search_control = _collection_search_control


class ChangeSetHasChangeFilter(UserFilter):

    id = "changeset-change"

    @cached_getter
    def schema(self):
        return schema.Schema("ChangeSetHasChangeFilter", members = [
            schema.Reference(
                "target",
                type = Item
            ),
            schema.Reference(
                "target_type",
                class_family = Item
            ),
            schema.String(
                "action",
                enumeration = ["create", "modify", "delete"],
                translate_value = lambda value, language = None, **kwargs:
                    translations(
                        "ChangeSetHasChangeFilter.action=none",
                        language,
                        **kwargs
                    )
                    if not value
                    else translations(
                        "woost %s action" % value,
                        language,
                        **kwargs
                    )
            )
        ])

    @getter
    def expression(self):
        return ChangeSetHasChangeExpression(
            self.target or self.target_type,
            self.action,
            include_implicit = False
        )

user_filters_registry.add(ChangeSet, ChangeSetHasChangeFilter)

user_filters_registry.add(Publishable, DescendsFromFilter)
user_filters_registry.set_filter_parameter(
    Publishable,
    DescendsFromFilter,
    "relation", Document.children
)

