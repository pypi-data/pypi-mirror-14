#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from json import dumps
from woost.models import Configuration

def add_event(
    element,
    category,
    action,
    label = None,
    value = None
):
    api = Configuration.instance.google_analytics_api

    if api == "ga.js":

        event_command = [
            '_trackEvent',
            category,
            action
        ]

        if label is not None:
            event_command.append(label)

        if value is not None:
            event_command.append(value)

        element.add_client_code(
            "jQuery(this).click(function () { _gaq.push(%s); });"
            % dumps(event_command)
        )

    elif api == "universal":

        event_data = {
            "hitType": "event",
            "eventCategory": category,
            "eventAction": action
        }

        if label is not None:
            event_data["eventLabel"] = label

        if value is not None:
            event_data["value"] = value

        element.add_client_code(
            "jQuery(this).click(function () { ga('send', %s); });"
            % dumps(event_data)
        )

