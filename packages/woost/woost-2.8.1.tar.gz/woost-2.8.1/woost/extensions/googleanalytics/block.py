#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import Block
from .utils import escape_ga_string, get_ga_value

base_init_view = Block.init_view

def init_view(self, view):

    if not view.ga_event_category:
        view.ga_event_category = get_ga_value(self.__class__)

    if not view.ga_event_action:
        view.ga_event_action = "click"

    if not view.ga_event_label:
        view.ga_event_label = get_ga_value(self)

    base_init_view(self, view)

Block.init_view = init_view

