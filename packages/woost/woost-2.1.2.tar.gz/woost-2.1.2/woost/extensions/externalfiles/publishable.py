#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from woost.models import Publishable, File, Configuration

_get_uri = Publishable.get_uri

def get_uri(
    self,
    path = None,
    parameters = None,
    language = None,
    host = None,
    encode = True
):
    if isinstance(self, File) and host in (None, "!", "?"):
        host = Configuration.instance.get_setting("external_files_host")

    return _get_uri(
        self,
        path = path,
        parameters = parameters,
        language = language,
        host = host,
        encode = encode
    )

Publishable.get_uri = get_uri

