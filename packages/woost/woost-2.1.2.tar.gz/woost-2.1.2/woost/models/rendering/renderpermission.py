#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models.permission import ContentPermission, ReadPermission
from woost.models.rendering.imagefactory import ImageFactory
from woost.models.messagestyles import permission_doesnt_match_style


class RenderPermission(ContentPermission):
    """Permission to obtain images representing instances of a content type."""

    instantiable = True

    factories = schema.Collection(
        items = schema.Reference(type = ImageFactory),
        related_end = schema.Collection(),
        edit_control = "cocktail.html.CheckList",
        searchable = False
    )

    def match(self, target, image_factory, verbose = False):

        if self.factories and image_factory not in self.factories:
            print permission_doesnt_match_style("factory doesn't match")
            return False

        return ContentPermission.match(self, target, verbose)

    @classmethod
    def permission_not_found(cls, user, verbose = False, **context):
        # If no specific render permission is found, a read permission will do
        return user.has_permission(
            ReadPermission,
            target = context["target"],
            verbose = verbose
        )

