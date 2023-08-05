#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from woost.models import Item, Configuration

_get_image_uri = Item.get_image_uri

def get_image_uri(
    self,
    image_factory = None,
    parameters = None,
    encode = True,
    include_extension = True,
    host = None
):
    if host in (None, "!", "?"):
        host = Configuration.instance.get_setting("external_files_host")

    return _get_image_uri(
        self,
        image_factory = image_factory,
        parameters = parameters,
        encode = encode,
        include_extension = include_extension,
        host = host
    )

Item.get_image_uri = get_image_uri
