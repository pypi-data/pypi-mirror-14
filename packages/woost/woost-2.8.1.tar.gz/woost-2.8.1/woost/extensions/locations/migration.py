#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pau Congost <pau.congost@whads.com>
"""
from cocktail.events import when
from cocktail.persistence import MigrationStep

step = MigrationStep("woost.extensions.locations: index Location.parent")

@when(step.executing)
def index_location_parent(e):
    from woost.extensions.locations.location import Location
    Location.parent.rebuild_index()

