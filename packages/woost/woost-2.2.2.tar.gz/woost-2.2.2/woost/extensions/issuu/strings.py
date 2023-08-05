#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations

# IssuuDocument
#------------------------------------------------------------------------------
translations.define("IssuuDocument",
    ca = u"Document Issuu",
    es = u"Documento Issuu",
    en = u"Issuu document"
)

translations.define("IssuuDocument-plural",
    ca = u"Documents Issuu",
    es = u"Documentos Issuu",
    en = u"Issuu documents"
)

translations.define("IssuuDocument.content",
    ca = u"Contingut",
    es = u"Contingut",
    en = u"Contingut"
)

translations.define("IssuuDocument.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("IssuuDocument.issuu_document_url",
    ca = u"URL document Issuu",
    es = u"URL documento Issuu",
    en = u"Issuu document URL"
)

translations.define("IssuuDocument.thumbnail_page",
    ca = u"Pàgina de la miniatura",
    es = u"Página de la miniatura",
    en = u"Thumbnail page"
)

translations.define("IssuuDocument.issuu_document_id",
    ca = u"ID document Issuu",
    es = u"ID documento Issuu",
    en = u"Issuu document ID"
)

translations.define("IssuuDocument.issuu_config_id",
    ca = u"ID configuració Issuu",
    es = u"ID configuración Issuu",
    en = u"Issuu config ID"
)

# IssuuBlock
#------------------------------------------------------------------------------
translations.define("IssuuBlock",
    ca = u"Document Issuu",
    es = u"Documento Issuu",
    en = u"Issuu document"
)

translations.define("IssuuBlock-plural",
    ca = u"Documents Issuu",
    es = u"Documentos Issuu",
    en = u"Issuu documents"
)

translations.define("IssuuBlock.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("IssuuBlock.issuu_document",
    ca = u"Document Issuu",
    es = u"Documento Issuu",
    en = u"Issuu document"
)

translations.define("woost.extensions.issuu.issuu_document_controller.title",
    ca = u"Controlador de document Issuu",
    es = u"Controlador de documento Issuu",
    en = u"Issuu document controller"
)

translations.define(
    "woost.extensions.issuu.issuudocument."
    "IssuuSearchAPIError-instance",
    ca = lambda instance: u"Error consulta a la Search API: <pre>%s</pre>"
                          % instance.response,
    es = lambda instance: u"Error consulta a la Search API: <pre>%s</pre>"
                          % instance.response,
    en = lambda instance: u"Issuu search API error: <pre>%s</pre>"
                          % instance.response
)

translations.define("IssuuBlock.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("IssuuBlock.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

# IssuuDocumentRenderer
#------------------------------------------------------------------------------
translations.define("IssuuDocumentRenderer",
    ca = u"Pintador de document Issuu",
    es = u"Pintador de documento Issuu",
    en = u"Issuu document renderer"
)

translations.define("IssuuDocumentRenderer-plural",
    ca = u"Pintador de documents Issuu",
    es = u"Pintador de documentos Issuu",
    en = u"Issuu documents renderer"
)

