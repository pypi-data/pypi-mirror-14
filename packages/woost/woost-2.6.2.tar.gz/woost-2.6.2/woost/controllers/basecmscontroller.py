#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2008
"""
from urllib import urlencode
import cherrypy
from cocktail.modeling import getter
from cocktail.events import event_handler
from cocktail.controllers import Controller, request_property
from cocktail.html import renderers, templates
from woost import app


class BaseCMSController(Controller):
    """Base class for all CMS controllers."""

    @request_property
    def view(self):
        if self.view_class:
            view = templates.new(self.view_class)
            cms = self.context["cms"]
            output = self.output
            cms.producing_output(controller = self, output = output)

            for key, value in output.iteritems():
                setattr(view, key, value)

            view.submitted = self.submitted
            view.successful = self.successful
            return view

    def _render_template(self):

        renderer = None
        format = self.rendering_format

        if format:
            if format == "html":
                format = "default"
            try:
                renderer = getattr(renderers, "%s_renderer" % format)
            except AttributeError:
                raise ValueError("Can't render '%s' using format '%s'"
                    % (template, format))

        if self.render_as_fragment:
            return self.view.render(renderer = renderer)
        else:
            return self.view.render_page(renderer = renderer)

    def application_uri(self, *args, **kwargs):
        """Builds an absolute URI from a set of path components and parameters.

        @param args: A set of path components, relative to the application
            root. Takes any object that can be expressed as an unicode string.

        @param kwargs: A set of query string parameters to be included on the
            generated URI.

        @return: The generated absolute URI.
        @rtype: unicode
        """
        path = (unicode(arg).strip("/") for arg in args)
        uri = (
            self.context["cms"].virtual_path
            + u"/".join(component for component in path if component)
        )

        if kwargs:
            uri += "?" + urlencode(
                dict(
                    (
                        key,
                        value.encode("utf-8")
                            if isinstance(value, unicode)
                            else value
                    )
                    for key, value in kwargs.iteritems()
                    if not value is None
                ),
                True
            )

        # Contextual URI prefix
        context_prefix = self.context.get("uri_prefix")

        if context_prefix:
            uri = context_prefix.rstrip("/") + "/" + uri.lstrip("/")

        if uri.startswith("./"):
            uri = uri[2:]

        return uri

    def contextual_uri(self, *args, **kwargs):
        """Builds an URI relative to the currently requested publishable item.

        @param args: A set of path components that will be appended to the
            publishable's URI. Accepts any object that can be expressed as an
            unicode string.

        @param kwargs: A set of query string parameters to be included on the
            generated URI.

        @return: The generated absolute URI.
        @rtype: unicode
        """
        publishable = self.context["publishable"]
        uri = app.url_resolver.get_path(publishable)

        if uri is None:
            return None

        return self.application_uri(
            uri,
            *args,
            **kwargs
        )

