#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import re
from cocktail import schema
from cocktail.controllers import Location
from woost.models.publishable import Publishable

video_id_expr = re.compile(r"www\.tv3\.cat/videos/(\d+)")

def extract_video_id(string):

    if string:
        match = video_id_expr.search(string)
        if match:
            return match.group(1)

    return string


class TV3ALaCartaVideo(Publishable):

    instantiable = True
    type_group = "resource"
    uri_pattern = "http://www.tv3.cat/videos/%s"
    video_player = "woost.extensions.tv3alacarta.TV3ALaCartaPlayer"

    default_resource_type = "video"

    members_order = ["title", "video_id"]

    title = schema.String(
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        member_group = "content"
    )

    video_id = schema.String(
        required = True,
        listed_by_default = False,
        normalization = extract_video_id,
        member_group = "content"
    )

    def get_uri(self,
        path = None,
        parameters = None,
        language = None,
        host = None,
        encode = True):
        return self.uri_pattern % self.video_id

    def is_internal_content(self, language = None):
        return False

