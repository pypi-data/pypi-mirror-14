#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.pkgutils import resolve
from cocktail import schema
from cocktail.persistence.query import Query
from cocktail.controllers import get_parameter, request_property
from cocktail.controllers.autocomplete import (
    MemberAutocompleteSource,
    AutocompleteController as BaseAutocompleteController,
)
from woost import app
from woost.models import (
    Item,
    Publishable,
    ReadPermission,
    PermissionExpression,
    IsAccessibleExpression
)


class CMSAutocompleteSource(MemberAutocompleteSource):

    publishable_check = False
    include_entry_type = True

    @request_property
    def items(self):
        items = MemberAutocompleteSource.items(self)
        user = app.user

        if self._listing_types:
            items = [
                item
                for item in items
                if user.has_permission(ReadPermission, target = item)
            ]
        else:
            if (
                self.publishable_check
                and issubclass(self.member.type, Publishable)
            ):
                items.add_filter(IsAccessibleExpression())
            else:
                items.add_filter(
                    PermissionExpression(
                        user,
                        ReadPermission
                    )
                )

        return items

    def get_entry(self, item):
        entry = MemberAutocompleteSource.get_entry(self, item)

        if self._listing_types:
            entry["icon"] = app.icon_resolver.find_icon_url(item, 16)
        else:
            entry["type"] = item.__class__.get_qualified_name(include_ns = True)

        return entry


class AutocompleteController(BaseAutocompleteController):

    def __init__(self, *args, **kwargs):
        BaseAutocompleteController.__init__(
            self,
            self._autocomplete_factory,
            *args,
            **kwargs
        )

    def _autocomplete_factory(self, query):
        autocomplete_class = resolve(self.member.autocomplete_class)
        return autocomplete_class(self.member, query)

    def __call__(self, member_ref, query = "", lang = None):
        self.member = get_parameter(
            schema.MemberReference(
                required = True,
                schemas = (Item,)
            ),
            source = lambda name: member_ref,
            errors = "raise"
        )
        return BaseAutocompleteController.__call__(self, query, lang)

