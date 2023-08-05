#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from glob import glob
from threading import Lock, Event
from cocktail.styled import styled
from cocktail.iteration import first
from cocktail.events import when
from cocktail.persistence import datastore
from woost import app
from woost.models import Configuration, File, User, ReadPermission
from woost.extensions.audio.audioencoder import AudioEncoder

_cache_lock = Lock()
_cache_ongoing_requests = {}

debug = False

def get_audio_uri(file, encoding):

    if isinstance(encoding, basestring):

        # Format requested by file extension
        if encoding.startswith("."):

            # The source file already matches the requested file extension,
            # use it as is
            if file.file_extension == encoding:
                return file.get_uri()

            # Otherwise, use the first encoder that matches the given file
            # extension
            encoder = first(
                enc
                for enc in Configuration.instance.audio_encoders
                if enc.extension == encoding
            )

        # Format requested by the user defined encoder ID (ie. mp3-128)
        else:
            encoder = AudioEncoder.require_instance(identifier = encoding)
    else:
        encoder = encoding

    if encoder is None:
        return None
    else:
        return "/audio/%d/%s%s" % (
            file.id,
            encoder.identifier,
            encoder.extension
        )

def request_encoding(file, encoder):

    if isinstance(encoder, basestring):
        encoder = AudioEncoder.require_instance(identifier = encoder)

    dest = get_audio_cache_dest(file, encoder)

    # The file hasn't been generated yet
    if not os.path.exists(dest):

        request = None
        request_key = (file.id, encoder.identifier)

        with _cache_lock:
            request = _cache_ongoing_requests.get(request_key)

            # Another thread is already requesting this file encoding: wait
            # for it to finish
            if request is not None:
                new_request = False
            # No other thread is generating the requested file/encoding
            # combination at present: generate it
            else:
                request = Event()
                _cache_ongoing_requests[request_key] = request
                new_request = True

                # Make sure the cache folder for the indicated file exists
                folder = app.path("audio-cache", str(file.id))

                if not os.path.exists(folder):
                    os.mkdir(folder)

        if new_request:
            try:
                encoder.encode(file, dest)
                with _cache_lock:
                    _create_symlink(file, dest)
                    request.set()
            finally:
                try:
                    del _cache_ongoing_requests[request_key]
                except KeyError:
                    pass
        else:
            request.wait()

    return dest

def get_audio_cache_dest(file, encoder):
    return app.path(
        "audio-cache",
        str(file.id),
        encoder.identifier + encoder.extension
    )

def _create_symlink(file, dest):
    """Create a symbolic link for static publication of an encoded file."""

    if not hasattr(os, "symlink"):
        return

    # Only create static publication links for public content
    anonymous = User.require_instance(qname = "woost.anonymous_user")
    if not anonymous.has_permission(ReadPermission, target = file):
        return

    static_folder = app.path("static", "audio", str(file.id))
    static_link = os.path.join(static_folder, os.path.basename(dest))

    if not os.path.lexists(static_link):

        # Make sure the containing folder exists
        if not os.path.exists(static_folder):
            os.mkdir(static_folder)

        os.symlink(dest, static_link)

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

def clear_audio_cache(item = None, encoder_id = None):

    if debug:
        from cocktail.styled import styled
        print styled("Clearing audio cache", "red"),

        if item:
            print styled("Item:", "light_gray"),
            print styled(item, "red", style = "bold"),

        if encoder_id:
            print styled("Encoder:", "light_gray"),
            print styled(encoder_id, "red", style = "bold"),

        print

    # Remove the full cache
    if item is None and encoder_id is None:
        _remove_dir_contents(app.path("audio-cache"))
        _remove_dir_contents(app.path("static", "audio"))

    # Selective drop: per item and/or encoder
    else:
        paths = []

        if item is not None:
            paths.append(app.path("audio-cache", str(item.id)))
            paths.append(app.path("static", "audio", str(item.id)))
        else:
            for base in (
                app.path("audio-cache"),
                app.path("static", "audio")
            ):
                for item in os.listdir(base):
                    path = os.path.join(base, item)
                    if os.path.isdir(path):
                        paths.append(path)

        if encoder_id is None:
            pattern = None
        else:
            pattern = encoder_id + ".*"

        for path in paths:
            _remove_dir_contents(path, pattern)

@when(File.changed)
@when(File.deleted)
def _clear_audio_cache_after_commit(event):
    item = event.source
    if item.is_inserted:
        clear_audio_cache_after_commit(item = item)

def clear_audio_cache_after_commit(item = None, encoder = None):

    if encoder:
        encoder_id = encoder.identifier
    else:
        encoder_id = None

    key = "woost.extensions.audio.request.clear_audio_cache(item=%s,encoder=%s)" % (
        item.id if item else "*",
        encoder_id or "*"
    )

    datastore.unique_after_commit_hook(
        key,
        _clear_audio_cache_after_commit_callback,
        item,
        encoder_id
    )

def _clear_audio_cache_after_commit_callback(
    commit_successful,
    item,
    encoder_id
):
    if commit_successful:
        clear_audio_cache(item, encoder_id)

