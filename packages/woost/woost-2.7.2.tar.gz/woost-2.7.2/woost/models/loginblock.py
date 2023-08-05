#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from cocktail import schema
from .block import Block
from .publishable import Publishable


class LoginBlock(Block):

    instantiable = True
    type_group = "blocks.forms"
    view_class = "woost.views.LoginBlockView"

    login_target = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        member_group = "content"
    )

    def init_view(self, view):
        Block.init_view(self, view)
        if self.login_target is not None:
            view["action"] = self.login_target.get_uri()
        if hasattr(cherrypy.request, "authentication_errors"):
            view.errors = cherrypy.request.authentication_errors

