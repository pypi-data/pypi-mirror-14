#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import urllib2
from bs4 import BeautifulSoup
from woost.models.configuration import Configuration
from woost.models.uri import URI, File


class URLImporter(object):

    def __init__(self):
        self.__handlers = []

    @property
    def handlers(self):
        return self.__handlers

    def prepend_handler(self, handler):
        self.__handlers.insert(0, handler)

    def append_handler(self, handler):
        self.__handlers.append(handler)

    def create_publishable(self, url, languages = None, timeout = 10):

        url_import = URLImport(self, url, languages, timeout)

        for handler in self.__handlers:
            publishable = handler(url_import)
            if publishable:
                return publishable

        return None


class URLImport(object):

    title = None
    description = None
    image_url = None
    mime_type = None
    response = None
    response_content = None
    soup = None

    def __init__(self, importer, url, languages, timeout = 10):

        self.importer = importer
        self.url = url
        self.languages = languages

        try:
            self.response = urllib2.urlopen(
                url,
                timeout = timeout
            )
            self.response_content = self.response.read()

            ct = self.response.headers.get("content-type")
            self.mime_type = ct.split(";")[0]

            if self.mime_type in ("text/html", "text/xhtml"):
                self.soup = BeautifulSoup(self.response_content)
        except:
            pass
        else:
            if self.soup:

                # Title
                title_tag = self.soup.find("meta", {"property": "og:title"})
                if title_tag:
                    self.title = title_tag["content"].strip()
                else:
                    title_tag = self.soup.find("title")
                    if title_tag:
                        self.title = title_tag.text.strip()

                # Description
                desc_tag = self.soup.find("meta", {"property": "og:description"})
                if desc_tag:
                    self.description = desc_tag["content"].strip()
                else:
                    desc_tag = self.soup.find("meta", {"name": "description"})
                    if desc_tag:
                        self.description = desc_tag["content"].strip()

                # Image
                image_tag = self.soup.find("meta", {"property": "og:image"})
                if image_tag:
                    self.image_url = image_tag["content"]

    def apply_scraped_info(self, publishable, image_member = "image"):
        publishable.mime_type = self.mime_type
        self.apply_title(publishable)
        self.apply_image(publishable, image_member)

    def apply_title(self, publishable):
        languages = self.languages or Configuration.instance.languages
        for language in languages:
            publishable.set("title", self.title, language)

    def apply_image(self, publishable, image_member = "image"):
        if (
            self.image_url
            and image_member
            and hasattr(publishable, image_member)
        ):
            image = File.from_path(self.image_url)
            setattr(publishable, image_member, image)


url_importer = URLImporter()

def import_url_as_uri(url_import):
    item = URI()
    url_import.apply_scraped_info(item)
    item.uri = url_import.url
    return item

url_importer.append_handler(import_url_as_uri)

