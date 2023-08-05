#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from ZODB.broken import Broken
from cocktail.persistence import datastore
from cocktail.persistence.utils import (
    is_broken,
    remove_broken_type as cocktail_remove_broken_type
)
from .item import Item
from .configuration import Configuration
from .permission import ContentPermission
from .changesets import Change
from .role import Role


def remove_broken_type(
    full_name,
    existing_bases = (),
    relations = (),
    excluded_relations = None,
    languages = None
):
    if languages is None:
        languages = Configuration.instance.languages

    if excluded_relations is None:
        excluded_relations = (Change.target,)

    cocktail_remove_broken_type(
        full_name,
        existing_bases = existing_bases,
        relations = relations,
        excluded_relations = excluded_relations,
        languages = languages
    )

    for role in Role.select():
        for cls in list(role.hidden_content_types):
            if (
                issubclass(cls, Broken)
                and cls.__module__ + "." + cls.__name__ == full_name
            ):
                role.hidden_content_types.remove(cls)

    for permission in ContentPermission.select():
        matching_items = permission.get("matching_items")
        if matching_items:
            type = matching_items.get("type")
            if type and type == full_name:
                permission.delete()

def delete_history():

    for item in Item.select():
        if not is_broken(item):
            try:
                del item._changes
            except AttributeError:
                pass

    for key in list(datastore.root):
        if key.startswith("woost.models.changesets."):
            del datastore.root[key]

