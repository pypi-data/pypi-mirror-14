#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from bs4 import BeautifulSoup, Comment
from woost.models import get_current_website

class HTMLAdapter(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        self.absolute_url_prefix = \
            "http://" + get_current_website().hosts[0]

    def adapt(self):

        # Remove all HTML comments
        is_comment = lambda text: isinstance(text, Comment)
        for comment in self.soup.findAll(text = is_comment):
            comment.extract()

        # Remove all scripts
        for element in self.soup.findAll("script"):
            element.extract()

        # Transform URLs
        for element in self.soup.findAll("a"):
            href = element.get("href")
            if href:
                element["href"] = self._transform_url(
                    href,
                    node = element
                )

        for element in self.soup.findAll("img"):
            src = element.get("src")
            if src:
                element["src"] = self._transform_url(
                    src,
                    node = element
                )

        return str(self.soup).decode("utf-8")

    def _transform_url(self, url, node = None):

        if url.startswith("mailto:"):
            return url

        # Make URLs absolute
        if "://" not in url:
            url = self.absolute_url_prefix + "/" + url.lstrip("/")

        return url

