#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
import cherrypy
from cocktail.translations import (
    get_language,
    set_language,
    clear_fallback_languages,
    set_fallback_languages
)
from cocktail.controllers import try_decode, context
from cocktail.controllers.parameters import set_cookie_expiration
from woost import app
from woost.models import Configuration


class LanguageScheme(object):

    cookie_duration = 60 * 60 * 24 * 15 # 15 days

    def process_request(self, path):

        self.setup_language_fallback_policy()

        if path:
            language = self.uri_component_to_language(path[0])
            if language in Configuration.instance.languages:
                path.pop(0)
            else:
                language = None
        else:
            language = None

        cherrypy.request.language_specified = (language is not None)

        if language is None:
            language = get_language() or self.infer_language()

        cherrypy.response.cookie["language"] = language
        cookie = cherrypy.response.cookie["language"]
        cookie["path"] = "/"
        set_cookie_expiration(cookie, seconds = self.cookie_duration)

        set_language(language)

    def infer_language(self):

        # Check for a language preference in a cookie
        cookie = cherrypy.request.cookie.get("language")

        if cookie:
            return cookie.value

        config = Configuration.instance

        # Check the 'Accept-Language' header sent by the client
        if config.get_setting("heed_client_language"):
            accept_language = cherrypy.request.headers.get("Accept-Language", None)

            if accept_language:
                available_languages = \
                    Configuration.instance.get_enabled_languages()
                best_language = None
                best_score = None

                for chunk in accept_language.split(","):
                    chunk = chunk.strip()
                    score = 1.0
                    chunk_parts = chunk.split(";")

                    if len(chunk_parts) > 1:
                        language = chunk_parts[0]
                        for part in chunk_parts[1:]:
                            if part.startswith("q="):
                                try:
                                    score = float(part[2:])
                                except TypeError:
                                    pass
                                else:
                                    break
                    else:
                        language = chunk

                    language = language.split('-', 1)[0]

                    if (
                        score
                        and language in available_languages
                        and (best_language is None or score > best_score)
                    ):
                        best_language = language
                        best_score = score

                if best_language:
                    return best_language

        # Fall back to the site's default language
        return config.get_setting("default_language")

    def translate_uri(self, path = None, language = None):

        current_language = get_language()

        if language is None:
            language = current_language

        if path is None:
            is_current_publishable = True
            path = cherrypy.request.path_info
            qs = cherrypy.request.query_string
        else:
            is_current_publishable = False
            qs = u""

        if isinstance(path, str):
            path = try_decode(path)

        if isinstance(qs, str):
            qs = try_decode(qs)

        if is_current_publishable and language != current_language:
            publishable = app.original_publishable or app.publishable
            current_uri = publishable.get_uri(
                language = current_language,
                encode = False
            )
            translation_uri = publishable.get_uri(language = language)
            path = path.replace(current_uri, translation_uri)
        else:
            path_components = path.strip("/").split("/")
            if (
                path_components
                and path_components[0] in Configuration.instance.languages
            ):
                path_components.pop(0)

            path_components.insert(0, self.language_to_uri_component(language))
            path = u"/" + u"/".join(path_components)

        return path + (u"?" + qs if qs else u"")

    def language_to_uri_component(self, language):
        return language

    def uri_component_to_language(self, uri_component):
        return uri_component

    def setup_language_fallback_policy(self):
        clear_fallback_languages()
        for language, fallback_languages \
        in Configuration.instance.fallback_languages:
            set_fallback_languages(language, fallback_languages)

