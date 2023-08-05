#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2013
"""
import urllib2
import cherrypy
from cocktail.events import event_handler
from cocktail import schema
from cocktail.translations import translations
from cocktail.persistence import transactional
from cocktail.controllers import request_property
from woost import app
from woost.models import (
    changeset_context,
    File,
    InstallationSyncPermission
)
from woost.models.synchronization import Synchronization
from woost.controllers.notifications import Notification
from woost.controllers.backoffice.editcontroller import EditController
from woost.controllers.backoffice.useractions import get_user_action


class InstallationSyncController(EditController):

    view_class = "woost.views.BackOfficeInstallationSyncView"

    @event_handler
    def handle_traversed(cls, e):
        app.user.require_permission(InstallationSyncPermission)

    @request_property
    def synchronization(self):
        site_installation = self.context["cms_item"]
        return Synchronization(
            site_installation.url,
            site_installation.synchronization_user,
            site_installation.synchronization_password
        )

    @request_property
    def comparision(self):
        try:
            return self.synchronization.compare_content(
                establish_relations = (self.sync_action == "sync")
            )
        except urllib2.HTTPError, e:
            self.sync_request_error = e
            return {"incomming": (), "modified": {}}

    @request_property
    def sync_request_error(self):
        return None

    @request_property
    def sync_action(self):
        return cherrypy.request.params.get("sync_action")

    @request_property
    def sync_selection(self):
        return cherrypy.request.params.get("sync_selection") or ()

    @request_property
    def submitted(self):
        return EditController.submitted(self) or self.sync_action

    def submit(self):
        if self.sync_action == "sync" and self.sync_request_error is None:
            self._synchronize()
        else:
            EditController.submit(self)

    @transactional()
    def _synchronize(self):
        cmp = self.comparision
        get_param = cherrypy.request.params.get
        file_downloads = set()
        selection = self.sync_selection

        with changeset_context(app.user):

            for obj in cmp["incomming"]:
                if obj.global_id in selection:
                    obj.insert()

                    if isinstance(obj, File):
                        file_downloads.add(obj)

            for global_id, change in cmp["modified"].iteritems():
                if global_id in selection:
                    local = change["local"]
                    remote = change["remote"]

                    for member, lang in change["diff"]:
                        value = schema.get(remote, member, language = lang)
                        local.set(member, value, lang)

                        if member in (File.file_hash, File.file_size):
                            file_downloads.add(local)

        # Download files from the remote copy
        for file in file_downloads:
            self.synchronization.download_file(file)

        # Find importable content again
        self.comparision = self.synchronization.compare_content()

        Notification(
            translations("woost.controllers.InstallationSyncController.success"),
            "success"
        ).emit()

    @request_property
    def output(self):
        output = EditController.output(self)
        output.update(self.comparision)
        output.update(
            selected_action = get_user_action("installation_sync"),
            sync_selection = self.sync_selection,
            sync_request_error = self.sync_request_error
        )
        return output

