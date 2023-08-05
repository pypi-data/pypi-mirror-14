#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.events import event_handler
from cocktail.translations import translations
from woost.controllers.backoffice.editstack import EditNode
from woost.controllers.notifications import notify_user


class CampaignMonitorListEditNode(EditNode):

    @event_handler
    def handle_committed(cls, event):

        item = event.source.item
        try:
            item.update()
        except Exception, e:
            notify_user(
                translations(
                    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode failed synchronization",
                    item = item,
                    exception = e
                ),
                "error",
                transient = False
            )
        else:
            notify_user(
                translations(
                    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode synchronized changes",
                    item = item
                ),
                "success"
            )
