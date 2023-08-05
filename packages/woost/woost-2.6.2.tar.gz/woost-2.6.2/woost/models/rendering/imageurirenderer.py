#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from urllib import urlopen
from httplib import HTTPConnection
from time import mktime, strptime
from cStringIO import StringIO
from PIL import Image
from cocktail import schema
from woost.models.uri import URI
from woost.models.rendering.renderer import Renderer


class ImageURIRenderer(Renderer):

    instantiable = True

    def can_render(self, item, **parameters):
        return isinstance(item, URI) and item.resource_type == "image"

    def get_item_uri(self, item):
        return item.uri

    def render(self, item, **parameters):

        # Open the remote resource
        uri = self.get_item_uri(item)
        http_resource = urlopen(uri)

        # Wrap image data in a buffer
        # (the object returned by urlopen() doesn't support seek(), which is
        # required by PIL)
        buffer = StringIO()
        buffer.write(http_resource.read())
        buffer.seek(0)

        return Image.open(buffer)

