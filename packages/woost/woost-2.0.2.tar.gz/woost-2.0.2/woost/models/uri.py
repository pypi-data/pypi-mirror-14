#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
from cocktail import schema
from cocktail.controllers import Location, make_uri
from woost.models.publishable import Publishable
from woost.models.controller import Controller
from woost.models.website import Website


class URI(Publishable):

    instantiable = True
    type_group = "resource"

    groups_order = ["content"]

    members_order = [
        "title",
        "uri",
        "language_specific_uri"
    ]

    default_controller = schema.DynamicDefault(
        lambda: Controller.get_instance(qname = "woost.uri_controller")
    )

    title = schema.String(
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        member_group = "content"
    )

    uri = schema.String(
        indexed = True,
        member_group = "content"
    )

    language_specific_uri = schema.String(
        translated = True,
        member_group = "content"
    )

    def get_uri(self,
        path = None,
        parameters = None,
        language = None,
        host = None,
        encode = True):

        uri = self.language_specific_uri or self.uri

        if uri is not None:

            if path:
                uri = make_uri(uri, *path)

            if parameters:
                uri = make_uri(uri, **parameters)

            uri = self._fix_uri(uri, host, encode)

        return uri

    def is_internal_content(self, language = None):

        uri = self.get_uri(host = "!", language = language)
        location = Location(uri)

        if not location.host:
            return True

        return any(
            location.host in website.hosts
            for website in Website.select()
        )

