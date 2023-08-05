#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
import cherrypy
from cocktail.translations import get_language, translations
from cocktail.modeling import cached_getter
from cocktail.controllers import get_state
from woost.controllers.publishablecontroller import PublishableController


class DocumentController(PublishableController):
    """A controller that serves rendered pages."""

    def __call__(self, **kwargs):

        # Document specified redirection
        document = self.context["publishable"]

        if document.redirection_mode:

            redirection_target = document.find_redirection_target()

            if redirection_target is None:
                raise cherrypy.NotFound()

            if redirection_target.is_internal_content():
                parameters = get_state()
            else:
                parameters = None

            uri = redirection_target.get_uri(parameters = parameters)
            method = document.redirection_method

            if method == "perm":
                raise cherrypy.HTTPRedirect(uri, 301)
            elif method == "client":
                return """
                    <!DOCTYPE html>
                    <html lang="%s">
                        <head>
                            <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
                            <meta http-equiv="refresh" content="1; url=%s"/>
                            <title>%s</title>
                        </head>
                        <body>
                            %s
                            <script type="text/javascript">
                                location.href = document.getElementById("woost-client-redirection").href;
                            </script>
                        </body>
                    </html>
                """ % (
                    get_language(),
                    uri,
                    translations("woost.controllers.DocumentController.redirection_title"),
                    translations(
                        "woost.controllers.DocumentController.redirection_explanation",
                        uri = uri
                    )
                )
            else:
                raise cherrypy.HTTPRedirect(uri)

        # No redirection, serve the document normally
        return PublishableController.__call__(self)

    @cached_getter
    def page_template(self):
        template = self.context["publishable"].template

        if template is None:
            raise cherrypy.NotFound()

        return template

    @cached_getter
    def view_class(self):
        return self.page_template.identifier

