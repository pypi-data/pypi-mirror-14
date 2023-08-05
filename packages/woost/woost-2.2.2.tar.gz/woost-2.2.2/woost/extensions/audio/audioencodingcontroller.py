#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os.path
from cocktail.controllers import serve_file
from woost.models import File
from woost.controllers.basecmscontroller import BaseCMSController
from woost.extensions.audio.request import request_encoding


class AudioEncodingController(BaseCMSController):

    def __call__(self, file_id, encoder_id):
        file = File.require_instance(int(file_id))
        encoder_id = os.path.splitext(encoder_id)[0]
        dest = request_encoding(file, encoder_id)
        return serve_file(dest)

