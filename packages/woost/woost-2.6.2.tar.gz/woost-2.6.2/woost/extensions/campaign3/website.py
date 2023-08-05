#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from woost.models import Website

Website.members_order.extend([
    "campaign_monitor_api_key",
    "campaign_monitor_client_id"
])

Website.add_member(
    schema.String("campaign_monitor_api_key",
        member_group = "services.campaign_monitor",
        listed_by_default = False
    )
)

Website.add_member(
    schema.String("campaign_monitor_client_id",
        member_group = "services.campaign_monitor",
        listed_by_default = False
    )
)

