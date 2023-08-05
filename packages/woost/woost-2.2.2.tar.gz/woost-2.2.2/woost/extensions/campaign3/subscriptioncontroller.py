#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
import cherrypy
from createsend import CreateSend, Subscriber, BadRequest
from cocktail import schema
from cocktail.pkgutils import import_object
from cocktail.controllers import (
    Controller,
    FormProcessor,
    Form,
    request_property
)
from woost.models import Configuration


class SubscriptionController(FormProcessor, Controller):

    class SubscriptionForm(Form):

        is_new = None

        @request_property
        def model(self):
            return import_object(self.controller.block.subscriber_model)

        @request_property
        def schema(self):
            adapted_schema = Form.schema(self)

            if len(self.controller.block.lists) > 1:
                lists = schema.Collection(
                    name = "lists",
                    items = schema.Reference(
                        type = "woost.extensions.campaign3.campaignmonitorlist.CampaignMonitorList"
                    ),
                    min = 1,
                    edit_control = "cocktail.html.CheckList",
                )
                adapted_schema.add_member(lists)
                self.adapter.exclude(lists.name)

            return adapted_schema

        @request_property
        def subscribed_lists(self):
            return self.data.get("lists") or self.controller.block.lists

        @request_property
        def email(self):
            return self.data["subscriber_email"]

        @request_property
        def name(self):
            return self.data["subscriber_name"]

        @request_property
        def custom_fields(self):
            return []

        def submit(self):
            Form.submit(self)
            for list in self.subscribed_lists:
                self.add_subscriber(list)

        def add_subscriber(self, list):
            subscriber = Subscriber(
                {"api_key": Configuration.instance.get_setting("campaign_monitor_api_key")}
            )

            # Check if the user is new to any list
            try:
                response = subscriber.get(list.list_id, self.email)
            except BadRequest:
                self.is_new = True
            else:
                if response.State != "Active":
                    self.is_new = True

            response = subscriber.add(
                list.list_id,
                self.email,
                self.name,
                self.custom_fields,
                True
            )

        def after_submit(self):
            # Redirect the user to the confirmation success page of the first
            # list if the subscriber is already subscribed to all lists
            if not self.is_new:
                for list in self.subscribed_lists:
                    if list.confirmation_success_page \
                    and list.confirmation_success_page.is_accessible():
                        raise cherrypy.HTTPRedirect(list.confirmation_success_page.get_uri())

            # Redirect the user to the confirmation page
            for list in self.subscribed_lists:
                if list.confirmation_page \
                and list.confirmation_page.is_accessible():
                    raise cherrypy.HTTPRedirect(list.confirmation_page.get_uri())

