#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
import re
from warnings import warn
from decimal import Decimal
from cocktail.modeling import classgetter
from cocktail.translations import (
    translations,
    require_language,
    set_language,
    set_fallback_languages
)
from cocktail import schema
from woost import app
from .item import Item
from .slot import Slot
from .publishable import Publishable
from .website import Website
from .websitesession import get_current_website
from .caching import CachingPolicy
from .rendering.renderer import Renderer
from .rendering.imagefactory import ImageFactory
from .videoplayersettings import VideoPlayerSettings
from .trigger import Trigger

try:
    from fractions import Fraction
except ImportError:
    _numerical_types = (int, float, Decimal)
else:
    _numerical_types = (int, float, Decimal, Fraction)


class Configuration(Item):

    instantiable = False

    type_group = "setup"

    groups_order = [
        "publication",
        "publication.pages",
        "publication.maintenance",
        "language",
        "media.images",
        "media.video",
        "rendering",
        "services",
        "system",
        "system.smtp",
        "admin"
    ]

    members_order = [
        "websites",
        "caching_policies",
        "down_for_maintenance",
        "maintenance_page",
        "maintenance_addresses",
        "login_page",
        "generic_error_page",
        "not_found_error_page",
        "forbidden_error_page",
        "languages",
        "published_languages",
        "default_language",
        "fallback_languages",
        "heed_client_language",
        "backoffice_language",
        "renderers",
        "image_factories",
        "video_player_settings",
        "timezone",
        "smtp_host",
        "smtp_port",
        "smtp_user",
        "smtp_password",
        "triggers"
    ]

    @classgetter
    def instance(cls):
        return cls.get_instance(qname = "woost.configuration")

    common_blocks = Slot()

    # publication
    #--------------------------------------------------------------------------
    websites = schema.Collection(
        items = schema.Reference(type = Website),
        related_end = schema.Collection(),
        integral = True,
        member_group = "publication"
    )

    caching_policies = schema.Collection(
        items = schema.Reference(type = CachingPolicy),
        integral = True,
        related_end = schema.Reference(),
        member_group = "publication"
    )

    login_page = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "publication.pages"
    )

    generic_error_page = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "publication.pages"
    )

    not_found_error_page = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "publication.pages"
    )

    forbidden_error_page = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        listed_by_default = False,
        member_group = "publication.pages"
    )

    down_for_maintenance = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "publication.maintenance"
    )

    maintenance_page = schema.Reference(
        type = "woost.models.Publishable",
        listed_by_default = False,
        member_group = "publication.maintenance"
    )

    maintenance_addresses = schema.Collection(
        items = schema.String(),
        listed_by_default = False,
        searchable = False,
        member_group = "publication.maintenance"
    )

    # language
    #------------------------------------------------------------------------------
    languages = schema.Collection(
        items = schema.String(
            format = "^[a-z]{2}(-[A-Z]{2})?(-[a-z]+)?$"
        ),
        min = 1,
        listed_by_default = False,
        searchable = False,
        member_group = "language"
    )

    published_languages = schema.Collection(
        items = schema.String(
            enumeration = languages,
            edit_control = "cocktail.html.TextBox"
        ),
        searchable = False,
        listed_by_default = False,
        member_group = "language"
    )

    default_language = schema.String(
        required = True,
        enumeration = languages,
        edit_control = "cocktail.html.TextBox",
        text_search = False,
        listed_by_default = False,
        searchable = False,
        member_group = "language"
    )

    fallback_languages = schema.Collection(
        items = (
            schema.Tuple(
                items = (
                    schema.String(enumeration = languages),
                    schema.Collection(
                        type = tuple,
                        items = schema.String(
                            enumeration = languages
                        ),
                        request_value_separator = ","
                    )
                ),
                request_value_separator = ":"
            )
        ),
        request_value_separator = "\n",
        edit_control = "cocktail.html.TextArea",
        searchable = False,
        member_group = "language"
    )

    def setup_languages(self):
        set_language(self.default_language)
        for language, fallback_languages in self.fallback_languages:
            set_fallback_languages(language, fallback_languages)

    heed_client_language = schema.Boolean(
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "language"
    )

    backoffice_language = schema.String(
        required = True,
        enumeration = ["en", "es", "ca"],
        default = "en",
        text_search = False,
        translate_value = lambda value, language = None, **kwargs:
            u"" if not value else translations(value, language, **kwargs),
        listed_by_default = False,
        member_group = "language"
    )

    # media
    #--------------------------------------------------------------------------
    renderers = schema.Collection(
        items = schema.Reference(type = Renderer),
        bidirectional = True,
        integral = True,
        related_end = schema.Reference(),
        member_group = "media.images"
    )

    image_factories = schema.Collection(
        items = schema.Reference(type = ImageFactory),
        bidirectional = True,
        integral = True,
        related_end = schema.Reference(),
        member_group = "media.images"
    )

    video_player_settings = schema.Collection(
        items = schema.Reference(type = VideoPlayerSettings),
        bidirectional = True,
        integral = True,
        related_end = schema.Reference(),
        member_group = "media.video"
    )

    # system
    #--------------------------------------------------------------------------
    timezone = schema.String(
        required = False,
        format = re.compile(r'^["GMT"|"UTC"|"PST"|"MST"|"CST"|"EST"]{3}$|^[+-]\d{4}$'),
        text_search = False,
        member_group = "system",
        listed_by_default = False
    )

    smtp_host = schema.String(
        default = "localhost",
        listed_by_default = False,
        text_search = False,
        member_group = "system.smtp"
    )

    smtp_port = schema.Integer(
        listed_by_default = False,
        member_group = "system.smtp"
    )

    smtp_user = schema.String(
        listed_by_default = False,
        text_search = False,
        member_group = "system.smtp"
    )

    smtp_password = schema.String(
        listed_by_default = False,
        text_search = False,
        member_group = "system.smtp"
    )

    # administration
    #--------------------------------------------------------------------------
    triggers = schema.Collection(
        items = schema.Reference(type = Trigger),
        related_end = schema.Reference(),
        integral = True,
        member_group = "administration"
    )

    def __translate__(self, language, **kwargs):
        return translations(self.__class__.__name__, language, **kwargs)

    def resolve_path(self, path):
        warn(
            "Configuration.resolve_path is deprecated, use app.url_resolver.resolve_path instead",
            DeprecationWarning,
            stacklevel = 2
        )
        return app.url_resolver.resolve_path(path)

    def get_path(self, publishable, language = None):
        warn(
            "Configuration.get_path is deprecated, use app.url_resolver.get_path instead",
            DeprecationWarning,
            stacklevel = 2
        )
        return app.url_resolver.get_path(publishable, language = language)

    def get_setting(self, key):
        """Obtains the value for the indicated configuration option.

        The method will search the active website first (see
        L{woost.models.get_current_website}), and the site's L{Configuration}
        if there is no active website, or if the website provides no
        significant value. Significant values include numbers, booleans, and
        any object that evaluates to True on a boolean context.

        @param key: The name of the value to obtain. Must match one of the
            members of the L{Configuration} or the L{Website} models.
        @type key: str

        @return: The value for the indicated configuration option.
        """
        website = get_current_website()

        if website is not None:
            value = getattr(website, key, None)
            if self._is_significant_setting_value(key, value):
                return value

        return getattr(self.instance, key, None)

    def _is_significant_setting_value(self, key, value):
        return value or isinstance(value, _numerical_types)

    def language_is_enabled(self, language = None):
        language_subset = self.get_setting("published_languages")
        if not language_subset:
            return True
        else:
            return require_language(language) in language_subset

    def get_enabled_languages(self):
        return self.get_setting("published_languages") or self.languages

    def connect_to_smtp(self):

        import smtplib

        port = self.get_setting("smtp_port") or smtplib.SMTP_PORT

        smtp = smtplib.SMTP(
            self.get_setting("smtp_host"),
            port
        )

        if port == 587:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

        user = self.get_setting("smtp_user")
        password = self.get_setting("smtp_password")

        if user and password:
            smtp.login(str(user), str(password))

        return smtp

    def get_website_by_host(self, host):

        # Specific match
        for website in self.websites:
            if host in website.hosts:
                return website

        # Partial wildcards (ie. *.foo.com)
        while True:
            pos = host.find(".")

            if pos == -1:
                break

            host = host[pos + 1:]
            wildcard = "*." + host
            for website in self.websites:
                if wildcard in website.hosts:
                    return website

        # Generic wildcard (*)
        for website in self.websites:
            if "*" in website.hosts:
                return website

