#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import abstractmethod
from cocktail import schema
from woost.models.item import Item


class Renderer(Item):

    instantiable = False
    visible_from_root = False

    title = schema.String(
        descriptive = True,
        translated = True
    )

    @abstractmethod
    def can_render(self, item, **parameters):
        """Indicates if the renderer is able to render the given item.

        @param item: The item to evaluate.
        @type item: L{Item<woost.models.item.Item>}

        @return: True if the renderer claims to be able to render the item,
            False otherwise.
        @rtype: bool
        """

    @abstractmethod
    def render(self, item, **parameters):
        """Produces an image for the given item.

        @param item: The item to render.
        @type item: L{Item<woost.models.item.Item>}

        @return: The image for the given item. If a suitable image file
            exists, the method should return a tuple consisting of a string
            pointing to its path and its MIME type. Otherwise, the method
            should craft the image in-memory and return it as an instance of
            the L{Image<Image.Image>} class.
        @rtype: tuple(str, str) or L{Image<Image.Image>}
        """

