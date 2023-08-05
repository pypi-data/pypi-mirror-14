#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from cocktail.controllers import Location
from woost.models import Publishable, url_importer


def extract_video_id(string):

    try:
        if string.startswith("http"):
            location = Location(string)
            return location.query_string["v"][0]
    except:
        pass

    try:
        if "youtu.be" in string:
            return string[string.rfind("/") + 1:]
    except:
        pass

    return None


class YouTubeVideo(Publishable):

    instantiable = True
    type_group = "resource"
    uri_pattern = "http://www.youtube.com/watch?v=%s"
    video_player = "cocktail.html.YouTubePlayer"

    default_resource_type = "video"

    members_order = ["title", "video_id"]

    title = schema.String(
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        spellcheck = True,
        member_group = "content"
    )

    video_id = schema.String(
        required = True,
        listed_by_default = False,
        normalization = lambda value: extract_video_id(value) or value,
        member_group = "content"
    )

    def get_uri(self,
        path = None,
        parameters = None,
        language = None,
        host = None,
        encode = True):
        return self.uri_pattern % (self.video_id,)

    def is_internal_content(self, language = None):
        return False


def import_url_as_yotube_video(url_import):

    video_id = extract_video_id(url_import.url)
    if video_id:
        item = YouTubeVideo()
        url_import.apply_scraped_info(item)
        item.video_id = video_id
        return item

    return None

url_importer.prepend_handler(import_url_as_yotube_video)

