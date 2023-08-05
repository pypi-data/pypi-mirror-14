#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from cocktail.events import event_handler
from cocktail import schema
from cocktail.translations import translations
from woost.models.item import Item
from woost.models.file import File
from woost.models.rendering.request import clear_image_cache_after_commit


class ImageEffect(Item):

    instantiable = False
    visible_from_root = False

    image_factory = schema.Reference(
        type = "woost.models.rendering.ImageFactory",
        bidirectional = True,
        visible = False
    )

    @event_handler
    def handle_changed(cls, e):
        if e.source.is_inserted and e.source.image_factory:
            clear_image_cache_after_commit(factory = e.source.image_factory)


class ImageSize(schema.String):

    @classmethod
    def resolve_size(cls, value, size):

        if isinstance(value, basestring):
            if value.endswith("%"):
                value = float(value.rstrip("%")) / 100
            elif "." in value:
                value = float(value)
            else:
                value = int(value)

        if isinstance(value, float):
            number = int(size * value)
        if value < 0:
            value += size

        return value


class HorizontalAlignment(schema.String):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("enumeration", ["left", "center", "right"])
        schema.String.__init__(self, *args, **kwargs)

    def translate_value(self, value, language = None, **kwargs):
        if not value:
            return ""
        else:
            return translations(
                "woost.models.rendering.horizontal_alignment=" + value,
                language,
                kwargs
            )


class VerticalAlignment(schema.String):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("enumeration", ["top", "center", "bottom"])
        schema.String.__init__(self, *args, **kwargs)

    def translate_value(self, value, language = None, **kwargs):
        if not value:
            return ""
        else:
            return translations(
                "woost.models.rendering.vertical_alignment=" + value,
                language,
                kwargs
            )


def resolve_color(value):

    if isinstance(value, basestring):

        value = value.lstrip("#")

        if len(value) in (3, 4):
            value = tuple(int(d * 2, 16) for d in value)
        elif len(value) == 6:
            value = (
                int(value[0:2], 16),
                int(value[2:4], 16),
                int(value[4:6], 16)
            )
        elif len(value) == 8:
            value = (
                int(value[0:2], 16),
                int(value[2:4], 16),
                int(value[4:6], 16),
                int(value[6:8], 16)
            )
        else:
            raise ValueError("Invalid color: " + value)

    return value


class Thumbnail(ImageEffect):

    instantiable = True

    members_order = [
        "width",
        "height"
    ]

    width = ImageSize()

    height = ImageSize()

    filter = Image.ANTIALIAS

    def apply(self, image):

        im_width, im_height = image.size

        width = self.width
        height = self.height

        if width is not None:
            width = ImageSize.resolve_size(width, im_width)

        if height is not None:
            height = ImageSize.resolve_size(height, im_height)

        if width is None:
            width = int(im_width * (float(height) / im_height))

        if height is None:
            height = int(im_height * (float(width) / im_width))

        image.thumbnail((width, height), self.filter)
        return image


class Crop(ImageEffect):

    instantiable = True

    members_order = [
        "left",
        "top",
        "right",
        "bottom"
    ]

    left = ImageSize()

    top = ImageSize()

    right = ImageSize()

    bottom = ImageSize()

    def apply(self, image):
        width, height = image.size
        return image.crop((
            ImageSize.resolve_size(self.left, width),
            ImageSize.resolve_size(self.top, height),
            ImageSize.resolve_size(self.right, width),
            ImageSize.resolve_size(self.bottom, height)
        ))


class Fill(ImageEffect):

    instantiable = True

    members_order = [
        "width",
        "height",
        "horizontal_alignment",
        "vertical_alignment",
        "preserve_vertical_images"
    ]

    width = ImageSize()

    height = ImageSize()

    horizontal_alignment = HorizontalAlignment(
        required = True,
        default = "center"
    )

    vertical_alignment = VerticalAlignment(
        required = True,
        default = "center"
    )

    preserve_vertical_images = schema.Boolean(
        required = True,
        default = True
    )

    filter = Image.ANTIALIAS

    def apply(self, image):

        source_width, source_height = image.size
        source_ratio = float(source_width) / source_height

        if self.preserve_vertical_images and source_ratio < 1:
            width = self.width or source_width
            height = self.height or source_height
            image.thumbnail(
                (
                    ImageSize.resolve_size(width, source_width),
                    ImageSize.resolve_size(height, source_height)
                ),
                self.filter
            )
            return image

        width = ImageSize.resolve_size(self.width, source_width)
        height = ImageSize.resolve_size(self.height, source_height)

        if width == source_width and height == source_height:
            return image

        target_ratio = float(width) / height

        if source_ratio > target_ratio:
            target_width = int(height * source_ratio)
            target_height = height
        else:
            target_width = width
            target_height = int(width * (1 / source_ratio))

        image.thumbnail((target_width, target_height), self.filter)

        if self.horizontal_alignment == "center":
            offset_x = (target_width - width) / 2
        elif self.horizontal_alignment == "left":
            offset_x = 0
        elif self.horizontal_alignment == "right":
            offset_x = target_width - width
        else:
            raise ValueError(
                "Fill.horizontal_alignment = %s not implemented"
                % self.horizontal_alignment
            )

        if self.vertical_alignment == "center":
            offset_y = (target_height - height) / 2
        elif self.vertical_alignment == "top":
            offset_y = 0
        elif self.vertical_alignment == "bottom":
            offset_y = target_height - height
        else:
            raise ValueError(
                "Fill.vertical_alignment = %s not implemented"
                % self.horizontal_alignment
            )

        thumbnail_width, thumbnail_height = image.size

        image = image.crop((
            min(offset_x, thumbnail_width),
            min(offset_y, thumbnail_height),
            min(width + offset_x, thumbnail_width),
            min(height + offset_y, thumbnail_height)
        ))

        return image


class Rotate(ImageEffect):

    instantiable = True

    angle = schema.Integer(
        required = True
    )

    filter = Image.BICUBIC

    def apply(self, image):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        return image.rotate(self.angle, self.filter, True)


class Color(ImageEffect):

    instantiable = True

    level = schema.Float(
        required = True
    )

    def apply(self, image):
        return ImageEnhance.Color(image).enhance(self.level)


class Brightness(ImageEffect):

    instantiable = True

    level = schema.Float(
        required = True
    )

    def apply(self, image):
        return ImageEnhance.Brightness(image).enhance(self.level)


class Contrast(ImageEffect):

    instantiable = True

    level = schema.Float(
        required = True
    )

    def apply(self, image):
        return ImageEnhance.Contrast(image).enhance(self.level)


class Sharpness(ImageEffect):

    instantiable = True

    level = schema.Float(
        required = True
    )

    def apply(self, image):
        return ImageEnhance.Sharpness(image).enhance(self.level)


class Frame(ImageEffect):

    instantiable = True

    members_order = [
        "edge_width",
        "edge_color",
        "vertical_padding",
        "horizontal_padding",
        "background"
    ]

    edge_width = schema.Integer(
        required = True,
        min = 1,
        default = 1
    )

    edge_color = schema.Color(
        required = True,
        default = "#000000"
    )

    vertical_padding = ImageSize(
        required = True,
        default = "0"
    )

    horizontal_padding = ImageSize(
        required = True,
        default = "0"
    )

    background = schema.Color(
        required = True,
        default = "#000000"
    )

    def apply(self, image):

        edge_color = resolve_color(self.edge_color)
        background = resolve_color(self.background)

        # Create the canvas
        width, height = image.size
        vertical_padding = ImageSize.resolve_size(self.vertical_padding, height)
        vertical_offset = self.edge_width + vertical_padding
        horizontal_padding = ImageSize.resolve_size(self.horizontal_padding, width)
        horizontal_offset = self.edge_width + horizontal_padding

        canvas = Image.new("RGBA", (
            width + horizontal_offset * 2,
            height + vertical_offset * 2
        ))

        # Paint the border
        edge = self.edge_width
        if edge:
            canvas.paste(edge_color, None)

        # Paint the padding color
        canvas.paste(
            background,
            (edge,
             edge,
             edge + width + horizontal_padding * 2,
             edge + height + vertical_padding * 2)
        )

        # Paste the original image over the frame
        canvas.paste(
            image,
            (horizontal_offset, vertical_offset),
            image if image.mode in ("1", "L", "RGBA") else None
        )

        return canvas


class Shadow(ImageEffect):

    instantiable = True

    offset = schema.Integer(
        required = True,
        default = 5
    )

    padding = schema.Integer(
        required = True,
        default = 8
    )

    color = schema.Color(
        required = True,
        default = "#444444"
    )

    iterations = 3

    def apply(self, image):

        # Create the backdrop image -- a box in the background colour with a
        # shadow on it.
        total_width = image.size[0] + abs(self.offset) + 2 * self.padding
        total_height = image.size[1] + abs(self.offset) + 2 * self.padding
        back = Image.new("RGBA", (total_width, total_height))

        # Place the shadow, taking into account the offset from the image
        shadow_left = self.padding + max(self.offset, 0)
        shadow_top = self.padding + max(self.offset, 0)
        color = resolve_color(self.color)
        back.paste(self.color, [
            shadow_left,
            shadow_top,
            shadow_left + image.size[0],
            shadow_top + image.size[1]
        ])

        # Apply the filter to blur the edges of the shadow.  Since a small
        # kernel is used, the filter must be applied repeatedly to get a
        # decent blur.
        for n in range(self.iterations):
            back = back.filter(ImageFilter.BLUR)

        # Paste the input image onto the shadow backdrop
        image_left = self.padding - min(self.offset, 0)
        image_top = self.padding - min(self.offset, 0)
        back.paste(
            image,
            (image_left, image_top),
            image if image.mode in ("1", "L", "RGBA") else None
        )

        return back


class ReducedOpacity(ImageEffect):
    """An image effect that reduces the opacity of the given image."""

    instantiable = True

    level = schema.Float(
        required = True,
        default = 0.5,
        min = 0.0,
        max = 1.0
    )

    def apply(self, image):
        return reduce_opacity(image, self.level)


def reduce_opacity(image, opacity):

    if opacity < 0 or opacity > 1:
        raise ValueError(
            "reduce_opacity() expects a floating point number "
            "between 0 and 1: got %s instead"
            % opacity
        )

    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    else:
        image = image.copy()

    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    image.putalpha(alpha)
    return image


class Fade(ImageEffect):

    instantiable = True

    members_order = [
        "top_width",
        "right_width",
        "bottom_width",
        "left_width"
    ]

    top_width = schema.Integer(
        required = True,
        default = 0,
        min = 0
    )

    right_width = schema.Integer(
        required = True,
        default = 0,
        min = 0
    )

    bottom_width = schema.Integer(
        required = True,
        default = 0,
        min = 0
    )

    left_width = schema.Integer(
        required = True,
        default = 0,
        min = 0
    )

    edge_opacity = schema.Integer(
        required = True,
        default = 0,
        min = 0,
        max = 255
    )

    inner_opacity = schema.Integer(
        required = True,
        default = 255,
        min = 0,
        max = 255
    )

    def apply(self, image):

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        pixels = image.load()
        w, h = image.size

        tw = self.top_width
        rw = self.right_width
        bw = self.bottom_width
        lw = self.left_width

        inner_opacity = self.inner_opacity
        edge_opacity = self.edge_opacity
        opacity_delta = self.inner_opacity - edge_opacity

        for x in xrange(w):
            for y in xrange(h):

                if x < lw:
                    hor_opacity = float(x) / lw
                elif x > w - rw:
                    hor_opacity = float(rw - (x - (w - rw))) / rw
                else:
                    hor_opacity = None

                if y < tw:
                    ver_opacity = float(y) / tw
                elif y > h - bw:
                    ver_opacity = float(bw - (y - (h - bw))) / bw
                else:
                    ver_opacity = None

                if hor_opacity is None and ver_opacity is None:
                    opacity = inner_opacity
                else:
                    if hor_opacity is None:
                        step = ver_opacity
                    elif ver_opacity is None:
                        step = hor_opacity
                    else:
                        step = min(ver_opacity, hor_opacity)

                    opacity = int(edge_opacity + opacity_delta * step)

                p = pixels[x, y]
                pixels[x, y] = (p[0], p[1], p[2], opacity)

        return image


class Watermark(ImageEffect):

    instantiable = True

    mark = schema.Reference(
        type = File,
        required = True,
        related_end = schema.Collection()
    )

    opacity = schema.Float(
        required = True,
        min = 0.0,
        max = 1.0,
        default = 1.0
    )

    placement = schema.String(
        required = True,
        default = "middle",
        enumeration = ["middle", "scale", "tile"]
    )

    def apply(self, image):

        mark_image = Image.open(self.mark.file_path)

        if self.opacity < 1:
            mark_image = reduce_opacity(mark_image, opacity)

        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Create a transparent layer the size of the image and draw the
        # watermark in that layer.
        layer = Image.new('RGBA', image.size, (0,0,0,0))

        if self.placement == 'tile':
            for y in range(0, image.size[1], mark_image.size[1]):
                for x in range(0, image.size[0], mark_image.size[0]):
                    layer.paste(mark_image, (x, y), mark_image)
        elif self.placement == 'scale':
            # scale, but preserve the aspect ratio
            ratio = min(
                float(image.size[0]) / mark_image.size[0],
                float(image.size[1]) / mark_image.size[1]
            )
            w = int(mark_image.size[0] * ratio)
            h = int(mark_image.size[1] * ratio)
            mark_image = mark_image.resize((w, h))
            layer.paste(
                mark_image,
                ((image.size[0] - w) / 2, (image.size[1] - h) / 2),
                mark_image
            )
        elif self.placement == 'middle':
            layer.paste(
                mark_image,
                (
                    (image.size[0] - mark_image.size[0]) / 2,
                    (image.size[1] - mark_image.size[1]) / 2
                ),
                mark_image
            )
        else:
            raise ValueError(
                "Must specify position parameter [tile,scale,middle]."
            )

        # composite the watermark with the layer
        return Image.composite(layer, image, layer)


class Flip(ImageEffect):

    instantiable = True

    axis = schema.String(
        required = True,
        edit_control = "cocktail.html.RadioSelector",
        enumeration = ["horizontal", "vertical"]
    )

    def apply(self, image):

        if self.axis == "horizontal":
            axis = Image.FLIP_LEFT_RIGHT
        elif self.axis == "vertical":
            axis = Image.FLIP_TOP_BOTTOM
        else:
            raise TypeError(
                "Flip.axis can either be 'horizontal' "
                "or 'vertical'; got %s." % self.direction
            )

        return image.transpose(axis)


class Align(ImageEffect):

    instantiable = True

    members_order = [
        "width",
        "height",
        "horizontal_alignment",
        "vertical_alignment",
        "background"
    ]

    width = ImageSize()

    height = ImageSize()

    horizontal_alignment = HorizontalAlignment(
        required = True,
        default = "center"
    )

    vertical_alignment = VerticalAlignment(
        required = True,
        default = "center"
    )

    background = schema.Color()

    def apply(self, image):

        source_width, source_height = image.size
        width = ImageSize.resolve_size(self.width, source_width)
        height = ImageSize.resolve_size(self.height, source_height)

        needs_halign = (source_width < width)
        needs_valign = (source_height < height)

        if needs_halign or needs_valign:

            if self.background:
                background = resolve_color(self.background)
            elif image.mode == "RGBA":
                background = (0,0,0,0)
            else:
                background = (255,255,255)

            copy = Image.new(
                "RGBA" if background and len(background) == 4 else "RGB",
                (width, height),
                background
            )

            x = 0
            y = 0

            if needs_halign:
                if self.horizontal_alignment == "left":
                    pass
                elif self.horizontal_alignment == "center":
                    x = width / 2 - source_width / 2
                elif self.horizontal_alignment == "right":
                    x = width - source_width
                else:
                    raise ValueError(
                        "Align.horizontal_alignment expects 'left', 'center' "
                        "or 'right', got %s" % self.horizontal_alignment
                    )

            if needs_valign:
                if self.vertical_alignment == "top":
                    pass
                elif self.vertical_alignment == "center":
                    y = height / 2 - source_height / 2
                elif self.vertical_alignment == "bottom":
                    y = height - source_height
                else:
                    raise ValueError(
                        "Align.horizontal_alignment expects 'top', 'center' "
                        "or 'bottom', got %s" % self.vertical_alignment
                    )

            copy.paste(image, (x, y), image if image.mode == "RGBA" else None)
            return copy

        return image


class Grayscale(ImageEffect):

    instantiable = True

    def apply(self, image):
        return ImageOps.grayscale(image)

