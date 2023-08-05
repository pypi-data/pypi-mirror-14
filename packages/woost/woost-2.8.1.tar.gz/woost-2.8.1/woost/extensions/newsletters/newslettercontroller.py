#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Javier Marrero <javier.marrero@whads.com>
"""

import cherrypy
from bs4 import BeautifulSoup, Comment
from premailer import *
from cocktail.controllers import request_property, Location
from woost import app
from woost.models import ModifyPermission
from woost.controllers.documentcontroller import DocumentController


class NewsletterController(DocumentController):

    def process_newsletter_html(self, html):
        soup = BeautifulSoup(html)

        # Remove all HTML comments
        is_comment = lambda text: isinstance(text, Comment)
        for comment in soup.findAll(text = is_comment):
            comment.extract()

        # Remove all scripts
        for element in soup.findAll("script"):
            element.extract()

        html = str(soup).decode("utf-8")

        # Inline CSS & absolute URLs
        premailer = Premailer(
            html,
            base_url = unicode(Location.get_current_host())
        )
        html = premailer.transform()
        return html

    def _produce_content(self, **kwargs):
        content = DocumentController._produce_content(self, **kwargs)

        # Disable newsletter processing if we are "editing" it
        if not app.user.has_permission(
            ModifyPermission,
            target = app.publishable
        ):
            content = self.process_newsletter_html(content)

        return content

