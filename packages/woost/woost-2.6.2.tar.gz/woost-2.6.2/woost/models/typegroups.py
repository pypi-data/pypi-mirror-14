#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

_undefined = object()


class TypeGroup(object):

    def __init__(self, id, children = None):
        self.id = id
        self.__children = []
        if children is not None:
            for child in children:
                self.append(child)

    def __repr__(self):
        return "TypeGroup(%r)" % self.id

    def __translate__(self, language, **kwargs):
        return translations("woost.type_groups." + self.id, language, **kwargs)

    def append(self, child):
        self.__children.append(child)

    def insert(self, position, child):

        # Insert after / before an existing child
        if isinstance(position, basestring):
            parts = position.split()
            if len(parts) == 2:
                for index, existing_child in enumerate(self.__children):
                    if existing_child.id == parts[1]:
                        break
                if parts[0] == "before":
                    position = index
                elif parts[0] == "after":
                    position = index + 1

        if not isinstance(position, int):
            raise ValueError("Invalid position: %s" % position)

        self.__children.insert(position, child)

    def pop(self, child_id, default = _undefined):
        child = None

        for index, existing_child in enumerate(self.__children):
            if existing_child.id == child_id:
                child = existing_child
                break

        if child is not None:
            del self.__children[index]
            return child

        if default != _undefined:
            return default

        raise KeyError("Unknown type group: " + child_id)


    def remove(self, child):
        if isinstance(child, basestring):
            self.pop(child)
        else:
            self.__children.remove(child)

    def __iter__(self):
        return iter(self.__children)

    def __len__(self):
        return len(self.__children)

    def __contains__(self, child):
        if isinstance(child, basestring):
            child_id = child
            return any(child.id == child_id for child in self.__children)
        else:
            return child in self.__children

    def __getitem__(self, child_id):

        for child in self.__children:
            if child.id == child_id:
                return child

        raise KeyError("Unknown type group: " + child_id)

    def __delitem__(self, child):
        self.remove(child)

type_groups = TypeGroup("global", [
    TypeGroup("publishable", [
        TypeGroup("document"),
        TypeGroup("resource")
    ]),
    TypeGroup("setup", [
        TypeGroup("customization"),
        TypeGroup("users")
    ]),
    TypeGroup("misc")
])

block_type_groups = TypeGroup("blocks", [
    TypeGroup("blocks.content"),
    TypeGroup("blocks.layout"),
    TypeGroup("blocks.listings"),
    TypeGroup("blocks.social"),
    TypeGroup("blocks.forms"),
    TypeGroup("blocks.custom")
])

