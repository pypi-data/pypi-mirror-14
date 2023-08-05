#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from time import time, sleep
from subprocess import Popen, PIPE
from cocktail import schema
from woost.models.item import Item
from woost.extensions.audio.audiodecoder import AudioDecoder


class AudioEncoder(Item):

    instantiable = True
    visible_from_root = False
    resolution = 0.25

    members_order = [
        "identifier",
        "mime_type",
        "extension",
        "command",
        "timeout",
        "timeout_size_factor"
    ]

    identifier = schema.String(
        required = True,
        unique = True,
        indexed = True,
        normalized_index = False,
        descriptive = True
    )

    mime_type = schema.String(
        required = True
    )

    extension = schema.String(
        required = True
    )

    command = schema.String(
        required = True
    )

    timeout = schema.Integer(
        required = True,
        default = 60
    )

    timeout_size_factor = schema.Float(
        default = 10.0
    )

    def encode(self, file, dest):

        # Most encoders expect PCM wave files as input, so we start by finding
        # an appropiate decoder for the given file.
        mime_type = file.mime_type

        if mime_type == "audio/mp3":
            mime_type = "audio/mpeg"

        decoder = AudioDecoder.require_instance(mime_type = mime_type)

        # Next, we produce the command line instructions for the decoding /
        # encoding procedure, using a shell pipe.
        decode_command = decoder.command % file.file_path
        encode_command = self.command % dest
        command = decode_command + " | " + encode_command

        # Calculate the timeout, based on a base value incremented according to
        # a file size factor
        timeout = self.timeout

        if self.timeout_size_factor:
            size = file.file_size
            if size:
                timeout += size / (self.timeout_size_factor * 1024 * 1024)

        # Encode the file and save it to the indicated location
        proc = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        start = time()

        while proc.poll() is None:
            if time() - start > timeout:
                proc.terminate()
                raise AudioEncodingTimeoutError(
                    "The following audio encoding command exceeded its "
                    "timeout of %d seconds: %s" % (timeout, command)
                )
            sleep(self.resolution)

        if proc.returncode:
            raise AudioEncodingCommandError(
                "The following audio encoding command reported an error: "
                "%s\n%s" % (command, proc.stderr.read().strip())
            )


class AudioEncodingTimeoutError(IOError):
    """An exception raised when an audio encoding request exceeds its
    timeout.
    """

class AudioEncodingCommandError(OSError):
    """An exception raised when the underlying command used by an audio encoder
    reports an error.
    """

