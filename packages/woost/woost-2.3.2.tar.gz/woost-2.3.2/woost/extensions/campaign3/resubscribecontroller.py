#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from datetime import datetime
import cherrypy
from createsend import CreateSend, Client, List, Subscriber, BadRequest
from cocktail import schema
from cocktail.controllers import Controller, request_property
from cocktail.controllers.parameters import get_parameter
from woost.models import Configuration
from woost.extensions.campaign3.campaignmonitorlist import CampaignMonitorList


class ResubscribeController(Controller):

    max_seconds = 60 * 60
    resubscribed_lists = None

    def __init__(self):
        self.resubscribed_lists = []

    @request_property
    def email(self):
        return get_parameter(schema.String("email"))

    def resubscribe(self):
        cs = CreateSend(
            {"api_key": Configuration.instance.get_setting("campaign_monitor_api_key")}
        )
        now = datetime.now()

        for client in cs.clients():
            client = Client(
                {"api_key": Configuration.instance.get_setting("campaign_monitor_api_key")},
                client.ClientID
            )
            for list in client.lists():
                subscriber = Subscriber(
                    {"api_key": Configuration.instance.get_setting("campaign_monitor_api_key")}
                )
                try:
                    response = subscriber.get(list.ListID, self.email)
                except BadRequest:
                    continue

                date = datetime.strptime(response.Date, '%Y-%m-%d %H:%M:%S')
                diff = now - date
                if response.State != "Active" and (
                    date > now or diff.seconds < self.max_seconds
                ):
                    response = subscriber.add(
                        list.ListID,
                        self.email,
                        response.Name,
                        None,
                        True
                    )
                    self.resubscribed_lists.append(list.ListID)

    @request_property
    def action(self):
        return get_parameter("action")

    @request_property
    def submitted(self):
        return cherrypy.request.method == "POST" \
            and self.action == "resubscribe" \
            and self.email

    def submit(self):
        self.resubscribe()
        self.after_submit()

    def after_submit(self):
        # Redirect the user to the confirmation page
        for list_id in self.resubscribed_lists:
            list = CampaignMonitorList.get_instance(list_id = list_id)
            if list \
            and list.confirmation_page \
            and list.confirmation_page.is_accessible():
                raise cherrypy.HTTPRedirect(list.confirmation_page.get_uri())

    @request_property
    def output(self):
        output = Controller.output(self)
        output["email"] = self.email
        return output
