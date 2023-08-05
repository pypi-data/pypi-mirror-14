#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from __future__ import with_statement
from types import GeneratorType
from threading import Lock
from time import time, mktime
from datetime import datetime
from hashlib import md5
import cherrypy
from cherrypy.lib import cptools, http
from cocktail.caching import CacheKeyError
from woost import app
from woost.controllers import BaseCMSController


class PublishableController(BaseCMSController):
    """Base controller for all publishable items (documents, files, etc)."""

    cache_enabled = True

    cached_headers = (
        "Content-Type",
        "Content-Length",
        "Content-Disposition",
        "Content-Encoding",
        "Last-Modified",
        "ETag"
    )

    def __call__(self, **kwargs):
        content = self._apply_cache(**kwargs)

        if content is None:
            content = self._produce_content(**kwargs)

        return content

    def _apply_cache(self, **kwargs):

        publishable = self.context["publishable"]
        request = cherrypy.request
        response = cherrypy.response

        if not (
            self.cache_enabled
            and publishable.cacheable
            and request.method == "GET"
            and "original_publishable" not in self.context
        ):
            return None

        caching_context = {
            "request": request,
            "controller": self
        }

        policy = publishable.get_effective_caching_policy(
            **caching_context
        )

        if policy is None or not policy.cache_enabled:
            return None

        # Find the unique cache identifier for the requested content
        cache_key = repr(policy.get_content_cache_key(
            publishable,
            **caching_context
        ))

        # Server side cache
        if policy.server_side_cache:

            try:
                cached_response = app.cache.retrieve(cache_key)

            except CacheKeyError:
                content = self.__produce_response(**kwargs)
                view = self.view
                expiration = policy.get_content_expiration(
                    publishable,
                    base = view and view.cache_expiration,
                    **caching_context
                )
                tags = policy.get_content_tags(
                    publishable,
                    base = view and view.cache_tags,
                    **caching_context
                )

                if isinstance(content, GeneratorType):
                    content = "".join(content)

                # Collect headers that should be included in the cache
                headers = {}
                response_headers = cherrypy.response.headers

                for header_name in self.cached_headers:
                    header_value = response_headers.get(header_name)
                    if header_value:
                        headers[header_name] = header_value

                # Store the response in the cache
                app.cache.store(
                    cache_key,
                    (headers, content),
                    expiration = expiration,
                    tags = tags
                )
            else:
                headers, content = cached_response
                cherrypy.response.headers.update(headers)
        else:
            content = self.__produce_response(**kwargs)

        # Client side cache
        cptools.validate_etags()
        return content

    def __produce_response(self, **kwargs):
        content = self._produce_content(**kwargs)

        if isinstance(content, GeneratorType):
            content_bytes = "".join(
                chunk.encode("utf-8")
                    if isinstance(chunk, unicode)
                    else chunk
                for chunk in content
            )
        elif isinstance(content, unicode):
            content_bytes = content.encode("utf-8")
        else:
            content_bytes = content

        cherrypy.response.headers["ETag"] = md5(content_bytes).hexdigest()
        return content_bytes

    def _produce_content(self, **kwargs):
        return BaseCMSController.__call__(self, **kwargs)

