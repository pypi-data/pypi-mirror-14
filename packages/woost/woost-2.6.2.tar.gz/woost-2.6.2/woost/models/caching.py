#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from datetime import datetime, timedelta
from cocktail import schema
from cocktail.translations import get_language
from cocktail.caching import Cache
from cocktail.controllers import Location
from cocktail.persistence import datastore, PersistentMapping
from .item import Item
from .usersession import get_current_user


class CachingPolicy(Item):

    visible_from_root = False
    edit_form = "woost.views.CachingPolicyForm"

    groups_order = ["cache"]
    members_order = [
        "description",
        "important",
        "cache_enabled",
        "server_side_cache",
        "expiration_expression",
        "cache_tags_expression",
        "cache_key_expression",
        "condition"
    ]

    description = schema.String(
        descriptive = True,
        translated = True,
        spellcheck = True,
        listed_by_default = False
    )

    important = schema.Boolean(
        required = True,
        default = False
    )

    cache_enabled = schema.Boolean(
        required = True,
        default = True
    )

    server_side_cache = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False
    )

    expiration_expression = schema.CodeBlock(
        language = "python"
    )

    condition = schema.CodeBlock(
        language = "python"
    )

    cache_key_expression = schema.CodeBlock(
        language = "python"
    )

    cache_tags_expression = schema.CodeBlock(
        language = "python"
    )

    def applies_to(self, publishable, **context):
        expression = self.condition
        if expression:
            expression = expression.replace("\r", "")
            context["publishable"] = publishable
            exec expression in context
            return context.get("applies", False)

        return True

    def get_content_cache_key(self, publishable, **context):

        user = get_current_user()

        cache_key = (
            str(Location.get_current(relative = False)),
            None
            if user is None or user.anonymous
            else tuple(role.id for role in user.roles)
        )
        key_qualifier = None
        expression = self.cache_key_expression

        if expression:
            expression = expression.replace("\r", "")
            context["publishable"] = publishable
            exec expression in context
            key_qualifier = context.get("cache_key")
        else:
            request = context.get("request")
            if request:
                key_qualifier = tuple(request.params.items())

        if key_qualifier:
            cache_key = cache_key + (key_qualifier,)

        return cache_key

    def get_content_expiration(self, publishable, base = None, **context):

        expression = self.expiration_expression
        expiration = base

        if expression:
            expression = expression.replace("\r", "")
            context["expiration"] = expiration
            context["publishable"] = publishable
            context["datetime"] = datetime
            context["timedelta"] = timedelta
            exec expression in context
            expiration = context.get("expiration")

        return expiration

    def get_content_tags(self, publishable, base = None, **context):

        tags = publishable.get_cache_tags(
            language = context.get("language") or get_language()
        )

        tags.add(self.main_cache_tag)

        if base:
            tags.update(base)

        expression = self.cache_tags_expression
        if expression:
            context["tags"] = tags
            exec expression in context
            tags = context.get("tags")

        return tags


# Utility functions
#------------------------------------------------------------------------------
def normalize_invalidation_date(value):

    if isinstance(value, Item):
        value = value.last_update_time

    elif hasattr(value, "__iter__"):
        max_date = None
        for item in value:
            date = normalize_invalidation_date(item)
            if date is None:
                continue
            if max_date is None or date > max_date:
                max_date = date

        value = max_date

    return value

def latest(selectable, *args, **kwargs):

    if not args and not kwargs \
    and hasattr(selectable, "get_last_instance_change"):
        return selectable.get_last_instance_change()

    return (
        selectable.select(
            order = Item.last_update_time.negative(),
            range = (0, 1)
        )
        .select(*args, **kwargs)
    )

def menu_items(publishable):
    items = []

    while publishable is not None:
        if hasattr(publishable, "children"):
            items.extend(publishable.children)
        if publishable.parent is None:
            items.append(publishable)
        publishable = publishable.parent

    return items

def file_date(publishable):
    try:
        ts = os.stat(publishable.file_path).st_mtime
    except IOError, OSError:
        return None

    return datetime.fromtimestamp(ts)

