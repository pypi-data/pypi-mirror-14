#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""

# Renderers
from woost.models.rendering.renderer import Renderer
from woost.models.rendering.chainrenderer import ChainRenderer
from woost.models.rendering.imagefilerenderer import ImageFileRenderer
from woost.models.rendering.imageurirenderer import ImageURIRenderer
from woost.models.rendering.videofilerenderer import VideoFileRenderer
from woost.models.rendering.pdfrenderer import PDFRenderer
from woost.models.rendering.htmlrenderer import HTMLRenderer
from woost.models.rendering.iconrenderer import IconRenderer

# Image effects
from woost.models.rendering.imagefactory import ImageFactory
from woost.models.rendering.imageeffects import (
    ImageEffect,
    ImageSize,
    Thumbnail,
    Crop,
    Fill,
    Rotate,
    Color,
    Brightness,
    Contrast,
    Sharpness,
    Frame,
    Shadow,
    ReducedOpacity,
    Fade,
    Watermark,
    Flip,
    Align
)

# Image requests and caching
from woost.models.rendering.request import (
    require_rendering,
    clear_image_cache,
    clear_image_cache_after_commit,
    BadRenderingRequest
)

