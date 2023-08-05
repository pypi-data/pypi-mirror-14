#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from pkg_resources import resource_filename
from cocktail.caching import Cache


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

