#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from woost.models.rendering import ImageURIRenderer
from woost.extensions.youtube.youtubevideo import YouTubeVideo

THUMBNAIL_URL_PATTERN = "http://img.youtube.com/vi/%s/0.jpg"


class YouTubeVideoRenderer(ImageURIRenderer):

    def can_render(self, item, **parameters):
        return isinstance(item, YouTubeVideo) and item.video_id

    def get_item_uri(self, item):
        return THUMBNAIL_URL_PATTERN % item.video_id

