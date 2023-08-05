#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2009
"""
from datetime import datetime
from cStringIO import StringIO
import cherrypy
from cocktail.events import when
from cocktail.translations import translations
from cocktail import schema
from cocktail.controllers import request_property
from cocktail.controllers.formcontrollermixin import FormControllerMixin
from cocktail.persistence import datastore
from woost.models import Configuration, Publishable, get_current_user
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from woost.extensions.staticsite.staticsitedestination import StatusTracker
from woost.extensions.staticsite.exportationpermission import \
    ExportationPermission


class ExportStaticSiteController(
    FormControllerMixin,
    BaseBackOfficeController
):
    view_class = "woost.extensions.staticsite.ExportStaticSiteView"
    selection = None

    def __init__(self, *args, **kwargs):
        BaseBackOfficeController.__init__(self, *args, **kwargs)
        FormControllerMixin.__init__(self, *args, **kwargs)
        self.selection = self.params.read(
            schema.Collection("selection", items = schema.Reference(type = Publishable))
        )

    @request_property
    def eligible_destinations(self):
        from woost.extensions.staticsite import StaticSiteExtension
        extension = StaticSiteExtension.instance
        return [
            destination
            for destination in extension.destinations
            if get_current_user().has_permission(
                ExportationPermission,
                destination = destination
            )
        ]

    @request_property
    def eligible_snapshoters(self):
        from woost.extensions.staticsite import StaticSiteExtension
        extension = StaticSiteExtension.instance
        return extension.snapshoters

    @request_property
    def form_model(self):
        site_languages = Configuration.instance.languages
        return schema.Schema("ExportStaticSite", members = [
            schema.Reference(
                "snapshoter",
                type =
                    "woost.extensions.staticsite.staticsitesnapshoter."
                    "StaticSiteSnapShoter",
                required = True,
                enumeration = self.eligible_snapshoters,
                edit_control = "cocktail.html.RadioSelector",
                default = self.eligible_snapshoters[0]
            ),
            schema.Reference(
                "destination",
                type =
                    "woost.extensions.staticsite.staticsitedestination."
                    "StaticSiteDestination",
                required = True,
                enumeration = self.eligible_destinations,
                edit_control = "cocktail.html.RadioSelector",
                default = self.eligible_destinations[0]
            ),
            schema.Boolean(
                "update_only",
                required = True,
                default = True
            ),
            schema.Boolean(
                "follow_links",
                required = True,
                default = True
            )
        ])

    def submit(self):
        FormControllerMixin.submit(self)

        export_events = []
        tracker = StatusTracker()

        @when(tracker.file_processed)
        def handle_file_processed(event):
            if event.status == "failed":
                event.error_handled = True
            export_events.append(event)

        form = self.form_data

        user = get_current_user()
        user.require_permission(
            ExportationPermission,
            destination = form["destination"]
        )

        destination = form["destination"]
        snapshoter = form["snapshoter"]

        context = self.form_data.copy()

        exporter_context = destination.export(
            snapshoter,
            self.selection,
            update_only = form["update_only"],
            status_tracker = tracker,
            context = context
        )

        # View class
        self.view_class = destination.view_class(exporter_context)

        self.output["export_events"] = export_events
        self.output.update(
            **destination.output(exporter_context)
        )

        datastore.commit()

    @request_property
    def output(self):
        output = BaseBackOfficeController.output(self)
        output.update(
            selection = self.selection,
            eligible_destinations = self.eligible_destinations,
            eligible_snapshoters = self.eligible_snapshoters
        )
        return output

