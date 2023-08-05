#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from shutil import rmtree
from tempfile import mkdtemp
from subprocess import Popen, PIPE
from time import time, sleep
from PIL import Image
from cocktail import schema
from woost.models.file import File
from woost.models.rendering.renderer import Renderer


class PDFRenderer(Renderer):
    """A content renderer that handles pdf files."""

    instantiable = True

    command = schema.String(
        required = True
    )

    timeout = schema.Integer(
        required = True,
        default = 20
    )

    timeout_size_factor = schema.Float(
        default = 10.0
    )

    def can_render(self, item, **parameters):
        return (
            self.command
            and isinstance(item, File)
            and item.resource_type == "document"
            and item.file_name.split(".")[-1].lower() == "pdf"
        )

    def render(self, item, page = 1, **parameters):

        timeout = self.timeout

        # Increase the timeout for bigger files
        if self.timeout_size_factor:
            size = item.file_size
            if size:
                timeout += size / (self.timeout_size_factor * 1024 * 1024)

        RESOLUTION = 0.25
        temp_path = mkdtemp()

        try:
            temp_image_file = os.path.join(temp_path, "thumbnail.png")

            command = self.command % {
                "source": item.file_path,
                "dest": temp_image_file,
                "page": page
            }

            p = Popen(command, shell=True, stdout=PIPE)
            start = time()

            while p.poll() is None:
                if time() - start > timeout:
                    p.terminate()
                    raise IOError(
                        "PDF rendering timeout: '%s' took more than "
                        "%.2f seconds"
                        % (command, timeout)
                    )
                sleep(RESOLUTION)

            return Image.open(temp_image_file)

        finally:
            rmtree(temp_path)


class PDFTimeoutError(IOError):
    """An exception raised when a PDF rendering operation takes too long to
    complete.
    """


try:
    p = Popen(["which", "gs"], stdout=PIPE)
    output = p.communicate()[0].replace("\n", "")
except:
    pass
else:
    if output:
        PDFRenderer.command.default = (
            output + ' -dFirstPage=%(page)s -dLastPage=%(page)s'
            ' -sDEVICE=jpeg -o %(dest)s -dJPEGQ=95 -r150x150 %(source)s'
        )

