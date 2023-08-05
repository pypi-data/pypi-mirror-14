#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
import re
from os.path import splitext
from cocktail.modeling import abstractmethod, ListWrapper
from cocktail.stringutils import normalize
from cocktail.translations import translations, get_language
from cocktail.controllers import resolve_object_ref
from woost.models import Publishable, get_current_website


class URLResolver(object):

    _url_schemes = None

    def __init__(self):
        self._url_schemes = []
        self._url_schemes_wrapper = ListWrapper(self._url_schemes)

    @property
    def url_schemes(self):
        return self._url_schemes_wrapper

    def add_url_scheme(self, url_scheme):
        self._url_schemes.append(url_scheme)

    def remove_url_scheme(self, url_scheme):
        self._url_schemes.remove(url_scheme)

    def insert_url_scheme(self, index, url_scheme):
        self._url_schemes.insert(index, url_scheme)

    def resolve_path(self, path):
        """Determines the publishable item that matches the indicated path.

        This method identifies a matching publishable item by trying each
        url scheme defined by the site, in order. Once a scheme finds a
        matching item, the search concludes.

        See L{URLScheme.resolve_path} for more details on the resolution
        process.

        @param path: The path to evaluate; A list-like object describing a
            a path relative to the application's root.
        @type path: str list

        @return: A structure containing the matching item and its publication
            details. If no matching item can be found, None is returned
            instead.
        @rtype: L{PathResolution}
        """
        if not path:
            website = get_current_website()
            if website:
                return PathResolution(None, website.home)
        else:
            for url_scheme in self._url_schemes:
                resolution = url_scheme.resolve_path(path)
                if resolution is not None:
                    return resolution

    def get_path(self, publishable, language = None):
        """Determines the canonical path of the indicated item.

        This method queries each url scheme defined by the site, in
        order. Once a scheme yields a matching path, the search concludes. That
        first match will be considered the item's canonical path.

        See L{URLScheme.get_path} for more details on how paths for
        publishable items are determined.

        @param publishable: The item to get the canonical path for.
        @type publishable: L{Publishable<woost.models.publishable.Publishable>}

        @param language: The language to get the path in (some schemes produce
            different canonical paths for the same content in different
            languages).
        @type language: str

        @return: The publication path for the indicated item, relative to the
            application's root. If none of the site's url schemes can
            produce a suitable path for the item, None is returned instead.
        @rtype: unicode
        """
        # The path to the home page is always the application root
        if publishable.is_home_page():
            return ""

        for url_scheme in self._url_schemes:
            path = url_scheme.get_path(publishable, language)
            if path is not None:
                return path


class URLScheme(object):
    """Base class for all kinds of content url schemes."""

    @abstractmethod
    def resolve_path(self, path):
        """Determines the publishable item that matches the indicated path.

        @param path: The path to evaluate; A list-like object describing a
            a path relative to the application's root.
        @type path: str list

        @return: A structure containing the matching item and its publication
            details. If no matching item can be found, None is returned
            instead.
        @rtype: L{PathResolution}
        """

    @abstractmethod
    def get_path(self, publishable, language):
        """Determines the canonical path of the indicated item.

        @param publishable: The item to get the canonical path for.
        @type publishable: L{Publishable<woost.models.publishable.Publishable>}

        @param language: The language to get the path in. Some schemes produce
            different canonical paths for the same content in different
            languages.
        @type language: str

        @return: The publication path for the indicated item, relative to the
            application's root. If none of the site's publishing schemes can
            produce a suitable path for the item, None is returned instead.
        @rtype: unicode
        """

    def get_publishable_file_extension(self, publishable):
        return getattr(publishable, "file_extension", None)


class PathResolution(object):
    """A structure that provides publication information for an item.

    The L{URLScheme.resolve_path} and L{Configuration.resolve_path}
    methods use this class to wrap their return values.

    @var scheme: The publishing scheme used to resolve the publication details
        for the indicated path. This will only be set when calling
        L{Configuration.resolve_path}, to enable the caller to discern which of
        all the registered schemes handled the path's resolution.
    @type scheme: L{URLScheme}

    @var item: The publishable item that matches the indicated path.
    @type item: L{Publishable<woost.models.publishable.Publishable>}

    @var matching_path: The part of the evaluated path that was used by the
        publishing scheme to determine the matching item.
    @type matching_path: list

    @var extra_path: Additional path components that were not used by the
        publishing scheme when determining the path's matching item. This
        will be relayed to the item's handler when invoking the dispatching
        machinery.
    @type extra_path: list
    """
    scheme = None
    item = None
    matching_path = []
    extra_path = []

    def __init__(self,
        scheme,
        item,
        matching_path = None,
        extra_path = None):

        self.scheme = scheme
        self.item = item
        self.matching_path = matching_path if matching_path is not None else []
        self.extra_path = extra_path if extra_path is not None else []


class HierarchicalURLScheme(URLScheme):
    """A url scheme that publishes pages following a name hierarchy.

    The name hierarchy is defined by the L{path<woost.models.Page.path>},
    and L{parent<woost.models.publishable.Publishable.parent>} members of the
    L{Publishable<woost.models.publishable.Publishable>} class.
    """

    def resolve_path(self, path):

        remaining_path = list(path)
        extra_path = []

        while remaining_path:
            page = Publishable.get_instance(
                full_path = u"/".join(remaining_path)
            )
            if page:
                return PathResolution(
                    self,
                    page,
                    remaining_path,
                    extra_path
                )
            extra_path.append(remaining_path.pop())

    def get_path(self, publishable, language):
        return publishable.full_path


class IdURLScheme(URLScheme):
    """A url scheme that publishes items based on their id."""

    include_file_extensions = True

    def resolve_path(self, path):
        if path:
            if path:
                ref, ext = splitext(path[0])
                try:
                    id = int(ref)
                except:
                    pass
                else:
                    publishable = Publishable.get_instance(id)

                    if ext and (
                        not self.include_file_extensions
                        or ext != self.get_publishable_file_extension(publishable)
                    ):
                        return None

                    if publishable is not None:
                        return PathResolution(
                            self,
                            publishable,
                            [path[0]],
                            path[1:]
                        )

    def get_path(self, publishable, language):
        path = str(publishable.id)

        if self.include_file_extensions:
            ext = self.get_publishable_file_extension(publishable)
            if ext:
                path += ext

        return path


class DescriptiveIdURLScheme(URLScheme):
    """A url scheme that combines a unique identifier and a descriptive
    text fragment.

    @ivar word_separator: The character used to separate words on an item's
        title when crafting its descriptive fragment.
    @type word_separator: str

    @ivar id_regexp: The regular expression used to extract the unique
        identifier from an URI. The expression must define an 'id' named group.
    @type id_regexp: regular expression

    @param format: A python formatting string, used for composing an item's
        URI from its unique identifier and flattened title. Receives 'title'
        and 'id' parameters.
    @type format: str
    """
    id_separator = "_"
    word_separator = "-"
    id_regexp = re.compile(r"(.+_)?(?P<id>[^.]+)(?P<ext>\.[a-zA-Z0-9]+)?$")
    title_splitter_regexp = re.compile(r"\W+", re.UNICODE)
    format = "%(title)s%(separator)s%(id)d"
    normalize = False
    include_file_extensions = True

    _uri_encodings = ["utf-8", "iso-8859-1"]

    def resolve_path(self, path):

        if path:

            ref = path[0]

            # Try to decode the supplied URI using a selection of different
            # string encodings
            if not isinstance(ref, unicode):
                for encoding in self._uri_encodings:
                    try:
                        ref = ref.decode(encoding)
                    except UnicodeDecodeError, ex:
                        pass
                    else:
                        break
                else:
                    raise ex

            # Discard descriptive text
            match = self.id_regexp.match(ref)

            if match is None:
                return None
            else:
                id = match.group("id")

            publishable = resolve_object_ref(Publishable, id)

            if publishable is not None:

                # A file extension was provided, but either the scheme doesn't
                # accept them, or the selected item doesn't match the requested
                # file type: 404
                try:
                    ext = match.group("ext")
                except:
                    ext = None

                if ext and (
                    not self.include_file_extensions
                    or ext != self.get_publishable_file_extension(publishable)
                ):
                    return None

                return PathResolution(
                    self,
                    publishable,
                    [path[0]],
                    path[1:]
                )

    def get_path(self, publishable, language):

        if not language:
            language = get_language()

        if language:
            title = translations(publishable, language)
        else:
            title = None

        if title:
            if self.normalize:
                title = normalize(title)

            title = self.title_splitter_regexp.sub(
                self.word_separator,
                title
            )
            title = title.lower()
            ref = self.format % {
                "title": title,
                "id": publishable.id,
                "separator": self.id_separator
            }
        else:
            ref = str(publishable.id)

        if self.include_file_extensions:
            ext = self.get_publishable_file_extension(publishable)
            if ext:
                ref += ext

        return ref

