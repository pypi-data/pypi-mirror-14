#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail import schema
from cocktail.translations import translations
from woost.models import Configuration, Item
from createsend import CreateSend, List


class CampaignMonitorList(Item):

    edit_node_class = \
        "woost.extensions.campaign3.campaignmonitorlisteditnode.CampaignMonitorListEditNode"

    members_order = [
        "title",
        "list_id",
        "confirmation_page",
        "confirmation_success_page",
        "unsubscribe_page",
    ]

    title = schema.String(
        required = True,
        descriptive = True
    )

    list_id = schema.String(
        required = True,
        unique = True,
        text_search = False
    )

    confirmation_page = schema.Reference(
        type = "woost.models.Publishable",
        related_end = schema.Collection()
    )

    confirmation_success_page = schema.Reference(
        type = "woost.models.Publishable",
        related_end = schema.Collection()
    )

    unsubscribe_page = schema.Reference(
        type = "woost.models.Publishable",
        related_end = schema.Collection()
    )

    def update(self):
        list = List(
            {"api_key": Configuration.instance.get_setting("campaign_monitor_api_key")},
            self.list_id
        )
        details = list.details()

        if self.confirmation_success_page:
            confirmation_success_page = self.confirmation_success_page.get_uri(
                host = "."
            )
        else:
            confirmation_success_page = None

        if self.unsubscribe_page:
            unsubscribe_page = self.unsubscribe_page.get_uri(host = ".") + "?email=[email]"
        else:
            unsubscribe_page = None

        list.update(
            details.Title,
            unsubscribe_page,
            details.ConfirmedOptIn,
            confirmation_success_page,
            unsubscribe_setting=details.UnsubscribeSetting
        )

