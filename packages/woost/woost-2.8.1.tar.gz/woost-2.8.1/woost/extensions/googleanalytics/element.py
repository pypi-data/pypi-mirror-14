#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from json import dumps
from cocktail.html import Element
from .utils import get_ga_custom_values

Element.ga_event_category = None
Element.ga_event_action = None
Element.ga_event_label = None
Element.ga_event_value = None
Element.ga_event_source = None
Element.ga_event_env = None
Element.ga_event_overrides = None

Element._ga_event_data = None

def _get_element_ga_event_data(self):
    if self._ga_event_data is None and (
        self.ga_event_source
        or self.ga_event_overrides
    ):
        return get_ga_custom_values(
            self.ga_event_source,
            overrides = self.ga_event_overrides,
            env = self.ga_event_env
        )
    return self._ga_event_data

def _set_element_ga_event_data(self, data):
    self._ga_event_data = data

Element.ga_event_data = property(
    _get_element_ga_event_data,
    _set_element_ga_event_data
)

_base_ready_element = Element._ready

def _ready_element(self):

    _base_ready_element(self)

    self["data-ga-event-category"] = self.ga_event_category
    self["data-ga-event-action"] = self.ga_event_action
    self["data-ga-event-label"] = self.ga_event_label
    self["data-ga-event-value"] = self.ga_event_value

    data = self.ga_event_data
    if data:
        self["data-ga-event-data"] = dumps(data)

Element._ready = _ready_element

