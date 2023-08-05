#-*- coding: utf-8 -*-
"""

@author:		Marc Pérez
@contact:		marc.perez@whads.com
@organization:	Whads/Accent SL
@since:			December 2009
"""
from cocktail.modeling import ListWrapper
from cocktail.translations import translations, get_language
from cocktail import schema
from woost.models import Extension, Configuration

translations.define("GoogleSearchExtension",
    ca = u"Cercador de Google",
    es = u"Buscador de Google",
    en = u"Google search"
)

translations.define("GoogleSearchExtension-plural",
    ca = u"Cercadors de Google",
    es = u"Buscadores de Google",
    en = u"Google search"
)


class GoogleSearchExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Proporciona els elements essencials per implementar el cercador
            de Google""",
            "ca"
        )
        self.set("description",
            u"""Proporciona los elementos esenciales para implementar el
            buscador de Google""",
            "es"
        )
        self.set("description",
            u"""Provides the essential elements to set up Google Search""",
            "en"
        )

    def _load(self):
        from woost.extensions.googlesearch import (
            strings,
            configuration,
            website
        )

    def search(self,
        query,
        page = 0,
        page_size = 10,
        language = None,
        filter = True,
        results_per_page = None):
        """Returns Google CSE results for the given query.

        @param query: The query to search.
        @type query: unicode

        @param page: The ordinal index of the results page to return, starting
            at 0.
        @type page: int

        @param page_size: The maximum number of results per page.
        @type page_size: int

        @param language: Restricts search results to matches for the given
            language. The language must be indicated using a two letter ISO
            language code.
        @type language: str

        @param filter: Indicates if Google should apply filtering over the
            search results (ie. to remove redundant matches).
        @type filter: bool

        @return: The results for the given query.
        @rtype: L{GoogleSearchResultsList}
        """
        from woost.extensions.googlesearch.search import google_cse_search
        return google_cse_search(
            Configuration.instance.get_setting("google_search_engine_id"),
            query,
            page = page,
            page_size = page_size,
            language = language,
            filter = filter,
            results_per_page = results_per_page
        )

