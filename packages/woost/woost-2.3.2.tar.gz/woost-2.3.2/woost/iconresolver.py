#-*- coding: utf-8 -*-
"""
Classes for choosing icons for CMS items.

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			April 2009
"""
import os
from pkg_resources import resource_filename
from cocktail.typemapping import TypeMapping
from cocktail.resourceloader import ResourceLoader
from cocktail.persistence import PersistentObject
from woost.models.website import Website
from woost.models.item import Item
from woost.models.publishable import Publishable
from woost.models.document import Document
from woost.models.file import File


class IconResolver(object):
    """An object that chooses icons for CMS items.

    @ivar icon_format: The image format that icons are stored in. Takes the
        same values accepted by PIL images.
    @type icon_format: str

    @ivar icon_repositories: A list of the directory/URL tuples to search for
        icons, in descending order of preference.
    @type icon_repositories: str list

    @ivar file_resolvers: A mapping of types and icon resolution functions.
        This allows to override the icon resolution machinery for certain
        content types. Resolution functions should take as parameters a content
        type and (optionally) an item, and return a list of possible icon file
        names that would be a match for them.
    @type file_resolvers: (L{Item<woost.models.Item>} class, callable)
        L{TypeMapping<cocktail.typemapping.TypeMapping>}

    @ivar name_resolution_cache: A cache that stores the result of the
        L{find_icon} method given a list of possible names produced by the
        L{file_resolvers} mapping.
    @type: L{ResourceLoader<cocktail.resourceloader.ResourceLoader>}
    """
    icon_format = "png"
    _icon_extension = None
    icon_repositories = []
    file_resolvers = None
    name_resolution_cache = None

    def __init__(self):
        self.icon_repositories = [
            (
                resource_filename("woost.views", "resources/images/icons"),
                "/resources/images/icons"
            )
        ]
        self.file_resolvers = TypeMapping()
        self.file_resolvers[Item] = self._resolve_item
        self.file_resolvers[Publishable] = self._resolve_publishable
        self.file_resolvers[Document] = self._resolve_document
        self.file_resolvers[File] = self._resolve_file
        self.name_resolution_cache = ResourceLoader(load = self._find_icon)

    def _get_icon_extension(self):
        return self._icon_extension or self.icon_format

    def _set_icon_extension(self, extension):
        self._icon_extension = extension

    icon_extension = property(_get_icon_extension, _set_icon_extension,
        doc = """The file extension for icon files. If a explicit value is not
        provided, it will be infered from L{icon_format}.
        @type: str
        """)

    def find_icon(self, item, size):
        """Obtains the path to the icon file that best represents the indicated
        CMS item or content type.

        The default implementation searches for icons in the directories
        specified by the L{icon_repositories} property, in order, returning the
        first icon whose name matches the name of one of the item's classes.
        Also, publishable items and files are special cased, to take their
        resource and MIME types into account.

        @param item: The item or content type to obtain the icon for.
        @type item: L{Item<woost.models.Item>} instance or class

        @param size: The size of the icon to look for, in pixels.
        @type size: int

        @return: The path to the best matching icon, or None if no matching
            icon is found.
        @rtype: str
        """
        if isinstance(item, type):
            content_type = item
            item = None
        else:
            content_type = item.__class__

        file_resolver = self.file_resolvers.get(content_type)

        if file_resolver is not None:
            file_names = file_resolver(content_type, item)
            if file_names:
                key = (size, tuple(file_names))
                return self.name_resolution_cache.request(key)

        return None

    def find_icon_path(self, item, size):
        match = self.find_icon(item, size)
        if match:
            return match[0]

    def find_icon_url(self, item, size):
        match = self.find_icon(item, size)
        if match:
            return match[1]

    def _find_icon(self, key):

        size, file_names = key

        repositories = self.icon_repositories
        size_str = "%dx%d" % (size, size)
        icon_ext = "." + self.icon_extension

        for repo_path, repo_url in repositories:
            for file_name in file_names:
                icon_path = os.path.join(
                    repo_path,
                    size_str,
                    file_name + icon_ext
                )
                if os.path.exists(icon_path):
                    icon_url = "%s/%s/%s" % (
                        repo_url.rstrip("/"),
                        size_str,
                        file_name + icon_ext
                    )
                    return (icon_path, icon_url)

        return None

    def _resolve_item(self, content_type, item):
        return [
            "type-" + cls.full_name.replace(".", "-")
            for cls in content_type.ascend_inheritance(True)
            if cls is not PersistentObject
        ]

    def _resolve_publishable(self, content_type, item):
        file_names = self._resolve_item(content_type, item)

        if item is not None:

            # Use a distinct icon for home pages
            if item.is_home_page():
                file_names.insert(0, "home")

            # Apply icons based on the item's resource type (but icons for
            # subclasses of Publishable / File still take precedence)
            try:
                pos = file_names.index("type-woost-models-file-File")
            except ValueError:
                pos = file_names.index("type-woost-models-publishable-Publishable")

            if item.resource_type:
                file_names.insert(pos, "resource-type-" + item.resource_type)

        return file_names

    def _resolve_document(self, content_type, item):
        file_names = self._resolve_publishable(content_type, item)

        if item is not None and item.redirection_mode:
            file_names.insert(0, "redirection")

        return file_names

    def _resolve_file(self, content_type, item):
        file_names = self._resolve_publishable(content_type, item)

        if item is not None and item.mime_type:
            mime = item.mime_type.replace("/", "-").replace(".", "-")
            file_names.insert(0, "mime-" + mime)

        return file_names

