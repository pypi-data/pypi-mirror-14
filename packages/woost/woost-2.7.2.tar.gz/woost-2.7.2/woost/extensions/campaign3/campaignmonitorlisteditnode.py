#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.events import event_handler
from cocktail.translations import translations
from woost.controllers.backoffice.editstack import EditNode
from woost.controllers.notifications import Notification


class CampaignMonitorListEditNode(EditNode):

    @event_handler
    def handle_committed(cls, event):

        item = event.source.item
        try:
            item.update()
        except Exception, e:
            Notification(
                translations(
                    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode failed synchronization",
                    item = item,
                    exception = e
                ),
                "error"
            ).emit()
        else:
            Notification(
                translations(
                    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode synchronized changes",
                    item = item
                ),
                "success"
            ).emit()
