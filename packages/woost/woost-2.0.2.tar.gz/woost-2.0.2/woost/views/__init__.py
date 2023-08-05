#-*- coding: utf-8 -*-
u"""
(X)HTML templates for the CMS backend application.

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
from os import path as _path
from cocktail.html import Element
from cocktail.persistence import PersistentClass
from woost.models import Item

def depends_on(self, tag_source, cache_part = None):
    if tag_source is None:
        pass
    elif isinstance(tag_source, basestring):
        tag = tag_source
        if cache_part:
            tag += "-" + cache_part
        self.cache_tags.add(tag)
    elif isinstance(tag_source, Item):
        self.cache_tags.update(
            tag_source.get_cache_tags(cache_part = cache_part)
        )
        self.update_cache_expiration(
            tag_source.get_cache_expiration()
        )
    elif isinstance(tag_source, PersistentClass):
        tag = tag_source.full_name
        if cache_part:
            tag += "-" + cache_part
        self.cache_tags.add(tag)
        self.update_cache_expiration(tag_source.get_cache_expiration_for_type())
    else:
        for item in tag_source:
            self.depends_on(item)

Element.depends_on = depends_on

