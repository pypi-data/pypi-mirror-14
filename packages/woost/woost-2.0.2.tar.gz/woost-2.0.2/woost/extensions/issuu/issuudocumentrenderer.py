#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from woost.models.rendering import ImageURIRenderer
from woost.extensions.issuu.issuudocument import IssuuDocument

THUMBNAIL_URL_PATTERN = "http://image.issuu.com/%s/jpg/page_%s.jpg"


class IssuuDocumentRenderer(ImageURIRenderer):

    def can_render(self, item, **parameters):
        return isinstance(item, IssuuDocument) and item.issuu_document_id and item.thumbnail_page

    def get_item_uri(self, item):
        return THUMBNAIL_URL_PATTERN % (
            item.issuu_document_id,
            item.thumbnail_page
        )


