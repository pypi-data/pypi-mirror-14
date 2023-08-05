#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.pkgutils import resolve
from cocktail.html.autocomplete import Autocomplete as BaseAutocomplete


class Autocomplete(BaseAutocomplete):

    ajax_search = True
    ajax_search_threshold = 100

    def get_default_ajax_url(self):
        return (
            "/autocomplete/%s/QUERY"
            % self.member.original_member.get_qualified_name(include_ns = True)
        )

    def create_autocomplete_source(self):
        autocomplete_class = resolve(self.member.autocomplete_class)
        return autocomplete_class(self.member)

