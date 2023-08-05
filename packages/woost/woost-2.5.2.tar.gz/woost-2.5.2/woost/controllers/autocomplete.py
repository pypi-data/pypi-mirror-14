#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.pkgutils import resolve
from cocktail import schema
from cocktail.controllers import get_parameter, request_property
from cocktail.controllers.autocomplete import (
    MemberAutocompleteSource,
    AutocompleteController as BaseAutocompleteController,
)
from woost.models import (
    get_current_user,
    Item,
    Publishable,
    ReadPermission,
    PermissionExpression,
    IsAccessibleExpression
)


class MemberRestrictedAutocompleteSource(MemberAutocompleteSource):

    publishable_check = False

    @request_property
    def items(self):
        items = MemberAutocompleteSource.items(self)

        if (
            self.publishable_check
            and issubclass(self.member.type, Publishable)
        ):
            items.add_filter(IsAccessibleExpression())
        else:
            items.add_filter(
                PermissionExpression(
                    get_current_user(),
                    ReadPermission
                )
            )

        return items


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

    def __call__(self, member_ref, query = ""):
        self.member = get_parameter(
            schema.MemberReference(
                required = True,
                schemas = (Item,)
            ),
            source = lambda name: member_ref,
            errors = "raise"
        )
        return BaseAutocompleteController.__call__(self, query)

