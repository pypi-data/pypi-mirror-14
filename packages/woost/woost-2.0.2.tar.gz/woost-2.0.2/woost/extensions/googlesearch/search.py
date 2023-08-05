#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from xml.sax import parseString
from xml.sax.handler import ContentHandler
from urllib import urlopen, quote_plus
from cocktail.modeling import ListWrapper
from cocktail.translations import get_language

URL_TEMPLATE = (
    "http://www.google.com/cse"
    "?cx=%(search_engine_id)s"
    "&query=%(query)s"
    "&start=%(page)d"
    "&num=%(page_size)d"
    "&lr=%(language)s"
    "&filter=%(filter)d"
    "&client=google-csbe"
    "&output=xml_no_dtd"
    "&ie=utf8"
    "&oe=utf8"
)

def google_cse_search(
    search_engine_id,
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
    cse_url = URL_TEMPLATE % {
        "search_engine_id": search_engine_id,
        "query": quote_plus(query.encode("utf-8")),
        "page": page * page_size,
        "page_size": page_size,
        "language": language or get_language(),
        "filter": int(bool(filter))
    }

    f = urlopen(cse_url)
    xml_response = f.read()
    f.close()

    results = []

    parser = GoogleCSEXMLParser()
    parseString(xml_response, parser)

    return GoogleSearchResultsList(
        parser.results,
        page,
        page_size,
        parser.result_count
    )


class GoogleCSEXMLParser(ContentHandler):

    result_count = 0
    current_result = None
    status = None

    READING_TOTAL_COUNT = 1
    READING_TITLE = 2
    READING_URL = 3
    READING_CONTEXT = 4

    def __init__(self, *args, **kwargs):
        ContentHandler.__init__(self, *args, **kwargs)
        self.results = []

    def startElement(self, name, attrs):
        if name == "M":
            self.status = self.READING_TOTAL_COUNT
        elif name == "T":
            self.status = self.READING_TITLE
        elif name == "U":
            self.status = self.READING_URL
        elif name == "S":
            self.status = self.READING_CONTEXT
        elif name == "R":
            result = GoogleSearchResult()
            self.results.append(result)
            self.current_result = result

    def endElement(self, name):
        self.status = None
        if name == "R":
            self.current_result = None

    def characters(self, content):
        if self.status == self.READING_TOTAL_COUNT:
            self.result_count = int(content)
        elif self.status == self.READING_TITLE:
            self.current_result.title += content
        elif self.status == self.READING_URL:
            self.current_result.url += content
        elif self.status == self.READING_CONTEXT:
            self.current_result.context += content
            self.current_result.context = self.current_result.context.replace('<br>','')


class GoogleSearchResultsList(ListWrapper):

    def __init__(self, results, page, page_size, result_count):
        ListWrapper.__init__(self, results)
        self.page = page
        self.page_size = page_size
        self.result_count = result_count


class GoogleSearchResult(object):
    title = ""
    url = ""
    context = ""

