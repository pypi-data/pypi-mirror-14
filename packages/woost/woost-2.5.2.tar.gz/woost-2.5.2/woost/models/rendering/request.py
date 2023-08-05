#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from glob import glob
from shutil import rmtree, copy
from cocktail.events import when
from cocktail.persistence import datastore
from woost import app
from woost.models.item import Item
from woost.models.user import User
from woost.models.permission import RenderPermission
from woost.models.rendering.imagefactory import ImageFactory
from woost.models.rendering.formats import (
    mime_types_by_format,
    extensions_by_format,
    formats_by_extension,
    default_format
)

debug = False

def _remove_dir_contents(path, pattern = None):

    # os.path.lexists is not supported on windows
    from cocktail.styled import styled
    exists = getattr(os.path, "lexists", os.path.exists)

    if exists(path):

        if pattern:
            items = glob(os.path.join(path, pattern))
        else:
            items = os.listdir(path)

        for item in items:
            item_path = os.path.join(path, item)
            if debug:
                print styled(" " * 4 + item_path, "red")
            try:
                if os.path.isdir(item_path):
                    rmtree(item_path)
                else:
                    os.remove(item_path)
            except OSError, ex:
                if debug:
                    print styled(ex, "red")

def clear_image_cache(item = None, factory = None):

    if not app.root:
        return

    if debug:
        from cocktail.styled import styled
        print styled("Clearing image cache", "red"),

        if item:
            print styled("Item:", "light_gray"),
            print styled(item, "red", style = "bold"),

        if factory:
            print styled("Factory:", "light_gray"),
            print styled(factory, "red", style = "bold"),

        print

    # Remove the full cache
    if item is None and factory is None:
        _remove_dir_contents(app.path("image-cache"))
        _remove_dir_contents(app.path("static", "images"))

    # Selective drop: per item and/or factory
    else:
        paths = []

        if item is not None:
            paths.append(app.path("image-cache", str(item.id)))
            paths.append(app.path("static", "images", str(item.id)))
        else:
            for base in (
                app.path("image-cache"),
                app.path("static", "images")
            ):
                for item in os.listdir(base):
                    path = os.path.join(base, item)
                    if os.path.isdir(path):
                        paths.append(path)

        if factory is None:
            pattern = None
        else:
            pattern = factory + ".*"

        for path in paths:
            _remove_dir_contents(path, pattern)

@when(Item.changed)
@when(Item.deleted)
def _clear_image_cache_after_commit(event):
    if app.root:
        item = event.source
        if item.is_inserted:
            clear_image_cache_after_commit(item = item)

def clear_image_cache_after_commit(item = None, factory = None):

    if not app.root:
        return

    if factory:
        factory_identifier = (
            factory.identifier
            or "factory%d" % factory.require_id()
        )
    else:
        factory_identifier = None

    key = "woost.models.rendering.clear_image_cache(item=%s,factory=%s)" % (
        item.require_id() if item else "*",
        factory_identifier or "*"
    )

    datastore.unique_after_commit_hook(
        key,
        _clear_image_cache_after_commit_callback,
        item,
        factory_identifier
    )

def _clear_image_cache_after_commit_callback(commit_successful, item, factory):
    if commit_successful:
        clear_image_cache(item, factory)

def require_rendering(
    item,
    factory = None,
    format = None,
    parameters = None):

    ext = None

    if factory is None:
        factory = ImageFactory.require_instance(identifier = "default")

    if format is None:
        if not isinstance(item, type):
            ext = getattr(item, "file_extension", None)

            if ext is not None:
                format = formats_by_extension.get(ext.lstrip(".").lower())
                if format is None:
                    ext = None

    elif format not in mime_types_by_format:
        raise BadRenderingRequest("Invalid image format: %s" % format)

    if format is None:
        format = default_format

    if ext is None:
        ext = extensions_by_format[format]

    identifier = factory.identifier or "factory%d" % factory.id
    file_name = "%s.%s" % (identifier, ext)
    item_id = item.full_name if isinstance(item, type) else str(item.id)

    # If the image hasn't been generated yet, do so and store it in the
    # application's image cache
    image_cache_file = app.path("image-cache", item_id, file_name)

    if not os.path.exists(image_cache_file):

        # Generate the file
        image = factory.render(item)

        if not image:
            raise RenderError("Can't render %s" % item)

        # Store the generated image in the image cache
        try:
            os.mkdir(app.path("image-cache", item_id))
        except OSError:
            pass

        if isinstance(image, basestring):
            try:
                os.remove(image_cache_file)
            except OSError:
                pass

            if hasattr(os, "symlink"):
                os.symlink(image, image_cache_file)
            else:
                copy(image, image_cache_file)
        else:
            if format == 'JPEG' and image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA')
            elif format == 'PNG' and image.mode == "CMYK":
                image = image.convert('RGBA')

            # Obtain save options from the ImageFactory.options_code member
            # (users can supply a dictionary of options that will be forwarded
            # to Image.save()).
            save_options = {}
            options_code = factory.options_code

            if options_code:
                context = {
                    "options": save_options,
                    "factory": factory,
                    "format": format,
                    "image": image
                }
                label = "%s #%s.options_code" % (
                    factory.__class__.__name__,
                    factory.id
                )
                options = compile(factory.options_code, label, "exec")
                exec options in context

            # Save the image to the filesystem
            image.save(image_cache_file, format, **save_options)

    # If the image is accessible to anonymous users, create a link in the
    # application's static content folder (further requests will be served
    # by the web server, no questions asked).
    if hasattr(os, "symlink"):
        static_publication_link = \
            app.path("static", "images", item_id, file_name)

        if not os.path.lexists(static_publication_link):
            anonymous = User.require_instance(qname = "woost.anonymous_user")

            if anonymous.has_permission(
                RenderPermission,
                target = item,
                image_factory = factory
            ):
                try:
                    os.mkdir(app.path("static", "images", item_id))
                except OSError:
                    pass
                os.symlink(image_cache_file, static_publication_link)

    return image_cache_file


class BadRenderingRequest(Exception):
    """An exception raised when trying to render a piece of content using
    invalid parameters (ie. an unknown image format).
    """


class RenderError(Exception):
    """An exception raised when a request for a certain image can't be
    fulfilled (ie. because there is no content renderer that can handle the
    specified content).
    """

