#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.iteration import first
from cocktail import schema
from woost.extensions.locations.location import Location


class CountryReference(schema.Reference):

    def __init__(self, *args, **kwargs):
        kwargs["type"] = Location
        kwargs.setdefault("default_order", "location_name")

        constraints = kwargs.get("relation_constraints")
        if constraints is None:
            constraints = {}
            kwargs["relation_constraints"] = constraints

        constraints["location_type"] = "country"

        schema.Reference.__init__(self, *args, **kwargs)

    def normalization(self, value):

        if isinstance(value, basestring):
            country = first(
                Location.select({
                    "location_type": "country",
                    "code": value.upper()
                })
            )
            if country is not None:
                value = country

        return value

