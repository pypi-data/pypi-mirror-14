#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.html import templates
from cocktail.translations import translations
from cocktail.typemapping import TypeMapping
from woost.models import Configuration, Publishable, File


class ViewFactory(object):

    _type_mapping = None

    def __init__(self):
        self._type_mapping = TypeMapping()

    def _normalize_view(self, value, item, **parameters):

        if isinstance(value, basestring):
            view = templates.new(value)
            view.item = item
        elif isinstance(value, ViewFactory):
            view = value.create_view(item, **parameters)
        elif isinstance(value, type):
            view = value()
            view.item = item
        elif callable(value):
            view = value(item, parameters)

        # Set any remaining parameters as attributes of the resulting view
        if view:
            for key, value in parameters.iteritems():
                setattr(view, key, value)

        return view

    def create_view(self, item, **parameters):

        view = None

        for cls, handlers in self._type_mapping.iter_by_type(item.__class__):
            for id, handler in handlers:
                view = self._normalize_view(handler, item, **parameters)
                if view is not None:
                    return view

        raise ValueError(
            "Can't create view for item: %s" % item
        )

    def register(self, cls, id, handler):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        handlers.append((id, handler))

    def register_first(self, cls, id, handler):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        handlers.insert(0, (id, handler))

    def register_before(self, cls, anchor, id, handler):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        new_handlers = []
        added = False

        for prev_id, prev_handler in handlers:
            if prev_id == anchor:
                new_handlers.append((id, handler))
                added = True
            new_handlers.append((prev_id, prev_handler))

        self._type_mapping[cls] = new_handlers

        if not added:
            raise ValueError(
                "Can't register %s before %s: "
                "no such handler for type %s in %s"
                % (
                    id,
                    anchor,
                    cls,
                    self
                )
            )

    def register_after(self, cls, anchor, id, handler):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        new_handlers = []
        added = False

        for prev_id, prev_handler in handlers:
            new_handlers.append((prev_id, prev_handler))
            if prev_id == anchor:
                new_handlers.append((id, handler))
                added = True

        self._type_mapping[cls] = new_handlers

        if not added:
            raise ValueError(
                "Can't register %s after %s: "
                "no such handler for type %s in %s"
                % (
                    id,
                    anchor,
                    cls,
                    self
                )
            )

    def replace(self, cls, id, handler):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        replaced = False
        for i, handler_data in enumerate(handlers):
            prev_id, prev_handler = handler_data
            if prev_id == id:
                handlers[i] = (id, handler)
                replaced = True
                break

        if not replaced:
            raise ValueError(
                "Can't replace %s: "
                "no such handler for type %s in %s"
                % (
                    id,
                    cls,
                    self
                )
            )

    def unregister(self, cls, id):
        handlers = self._type_mapping.get(cls, recursive = False)
        if handlers is None:
            handlers = []
            self._type_mapping[cls] = handlers

        new_handlers = []

        for prev_id, prev_handler in handlers:
            if prev_id != id:
                new_handlers.append((prev_id, prev_handler))

        self._type_mapping[cls] = new_handlers


publishable_view_factory = ViewFactory()

def video_player(item, parameters):
    if item.resource_type == "video":

        player_settings = parameters.get("player_settings")

        if player_settings is None:
            player_settings_list = Configuration.instance.video_player_settings
            if player_settings_list:
                player_settings = player_settings_list[0]

        if player_settings:
            return player_settings.create_player(item)

publishable_view_factory.register(Publishable, "video_player", video_player)

def image_gallery(item, parameters):
    if (
        item.resource_type == "image"
        and not parameters.get("links_force_download", False)
    ):
        view = templates.new("woost.views.ImageGallery")
        view.images = [item]
        view.labels_visible = False
        return view

publishable_view_factory.register(Publishable, "image_gallery", image_gallery)

publishable_view_factory.register(
    Publishable,
    "default_thumbnail",
    "woost.views.ThumbnailLink"
)

publishable_grid_view_factory = ViewFactory()

def video_player_dialog(item, parameters):
    if (
        item.resource_type == "video"
        and (
            not isinstance(item, File)
            or not parameters.get("links_force_download", False)
        )
    ):
        view = templates.new("woost.views.PublishablePopUp")
        view.item = item
        view.view_factory = publishable_view_factory
        return view

publishable_grid_view_factory.register(
    Publishable,
    "video_player_dialog",
    video_player_dialog
)
publishable_grid_view_factory.register(
    Publishable,
    "publishable_view_factory",
    publishable_view_factory
)

