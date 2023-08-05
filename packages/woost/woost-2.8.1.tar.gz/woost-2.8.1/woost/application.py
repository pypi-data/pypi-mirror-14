#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from threading import local
from pkg_resources import resource_filename
from cocktail.modeling import GenericMethod
from cocktail.caching import Cache
from cocktail.controllers import context


class Application(object):

    __package = None
    __root = None
    __icon_resolver = None
    __custom_icon_repository = None

    __language = None
    __authentication = None

    installation_id = None
    installation_color = None

    splash = """\
Made with                     _
__        __ ___   ___   ___ | |_
\ \  __  / // _ \ / _ \ / __||  _|
 \ \/  \/ /| (_) | (_) |___ \| |__
  \__/\__/  \___/ \___/|____/\___/

http://woost.info
"""

    def __init__(self):
        self._thread_data = local()

    def path(self, *args):
        return os.path.join(self.root, *args)

    def _get_package(self):
        return self.__package

    def _set_package(self, package):
        self.__package = package
        self.__add_custom_icon_repository()

    package = property(_get_package, _set_package)

    def _get_root(self):
        if self.__root is None and self.__package:
            return resource_filename(self.__package, "")

        return self.__root

    def _set_root(self, root):
        self.__root = root
        self.__add_custom_icon_repository()

    root = property(_get_root, _set_root)

    def __add_custom_icon_repository(self):

        root = self.root
        package = self.package

        if root and package:
            repository = (
                self.path("views", "resources", "images", "icons"),
                "/" + self.package + "_resources/images/icons"
            )

            if (
                self.__custom_icon_repository is not None
                and self.__custom_icon_repository != repository
            ):
                self.icon_resolver.icon_repositories.remove(
                    self.__custom_icon_repository
                )

            self.__custom_icon_repository = repository
            self.icon_resolver.icon_repositories.insert(0, repository)

    @property
    def icon_resolver(self):
        if self.__icon_resolver is None:
            from woost.iconresolver import IconResolver
            self.__icon_resolver = IconResolver()
        return self.__icon_resolver

    # Language scheme
    def _get_language(self):
        if self.__language is None:
            from woost.languagescheme import LanguageScheme
            self.__language = LanguageScheme()
        return self.__language

    def _set_language(self, language):
        self.__language = language

    language = property(_get_language, _set_language)

    # Authentication scheme
    def _get_authentication(self):
        if self.__authentication is None:
            from woost.authenticationscheme import AuthenticationScheme
            self.__authentication = AuthenticationScheme()
        return self.__authentication

    def _set_authentication(self, authentication):
        self.__authentication = authentication

    authentication = property(_get_authentication, _set_authentication)

    # Caching
    cache = Cache()

    # URLs
    __url_resolver = None

    def _get_url_resolver(self):
        if self.__url_resolver is None:
            from woost.urlresolver import (
                URLResolver,
                HierarchicalURLScheme,
                DescriptiveIdURLScheme
            )
            url_resolver = URLResolver()
            url_resolver.add_url_scheme(HierarchicalURLScheme())
            url_resolver.add_url_scheme(DescriptiveIdURLScheme())
            self.__url_resolver = url_resolver
        return self.__url_resolver

    def _set_url_resolver(self, url_resolver):
        self.__url_resolver = url_resolver

    url_resolver = property(_get_url_resolver, _set_url_resolver)

    # Last error
    def _get_error(self):
        return getattr(self._thread_data, "error", None)

    def _set_error(self, error):
        self._thread_data.error = error

    error = property(_get_error, _set_error, doc =
        """Gets or sets the last error for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: Exception
        """
    )

    traceback_link_style = "disabled"

    # Last traceback
    def _get_traceback(self):
        return getattr(self._thread_data, "traceback", None)

    def _set_traceback(self, traceback):
        self._thread_data.traceback = traceback

    traceback = property(_get_traceback, _set_traceback, doc =
        """Gets or sets the last traceback for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: Traceback
        """
    )

    # Active user
    def _get_user(self):
        return getattr(self._thread_data, "user", None)

    def _set_user(self, user):
        self._thread_data.user = user

    user = property(_get_user, _set_user, doc =
        """Gets or sets the active user for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: `woost.models.User`
        """
    )

    # Active website
    def _get_website(self):
        return getattr(self._thread_data, "website", None)

    def _set_website(self, website):
        self._thread_data.website = website

    website = property(_get_website, _set_website, doc =
        """Gets or sets the active website for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: `woost.models.Website`
        """
    )

    # Active publishable
    def _get_publishable(self):
        return getattr(self._thread_data, "publishable", None)

    def _set_publishable(self, publishable):
        self._thread_data.publishable = publishable
        if self.original_publishable is None:
            self.navigation_point = get_navigation_point(publishable)

        # Required to preserve backward compatibility
        context["publishable"] = publishable

    publishable = property(_get_publishable, _set_publishable, doc =
        """Gets or sets the active publishable for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: `woost.models.publishable`
        """
    )

    # Active original publishable
    def _get_original_publishable(self):
        return getattr(self._thread_data, "original_publishable", None)

    def _set_original_publishable(self, original_publishable):
        self._thread_data.original_publishable = original_publishable
        self.navigation_point = get_navigation_point(original_publishable)

        # Required to preserve backward compatibility
        context["original_publishable"] = original_publishable

    original_publishable = property(
        _get_original_publishable,
        _set_original_publishable,
        doc = """
        Gets or sets the active original_publishable for the current context.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: `woost.models.original_publishable`
        """
    )

    # Active navigation point
    def _get_navigation_point(self):
        return getattr(self._thread_data, "navigation_point", None)

    def _set_navigation_point(self, navigation_point):
        self._thread_data.navigation_point = navigation_point

    navigation_point = property(_get_navigation_point, _set_navigation_point, doc =
        """Gets or sets the active navigation point for the current context.

        The navigation point is the publishable that should be highlighted as
        the active element in the navigation controls of the site's user
        interface. This will usually be the same as the active publishable,
        but not always: news items are a typical use case where the active
        publishable (the piece of news) and the highlighted page (the news
        listing) will differ.

        "Context" is typically an HTTP request, but the property can also be
        used outside a web request/response cycle.

        .. type:: `woost.models.navigation_point`
        """
    )


@GenericMethod
def get_navigation_point(self):
    return self

