#-*- coding: utf-8 -*-
u"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
import os
from shutil import move
import cherrypy
from cocktail.events import event_handler
from cocktail import schema
from cocktail.schema.exceptions import ValidationError
from cocktail.controllers import (
    context,
    session,
    request_property,
    FileUpload
)
from cocktail.controllers.fileupload import FileUpload
from woost import app
from woost.controllers.asyncupload import async_uploader
from woost.controllers.backoffice.editstack import EditNode


class FileEditNode(EditNode):

    @request_property
    def form_adapter(self):
        adapter = EditNode.form_adapter(self)
        adapter.exclude(["mime_type"])
        adapter.import_rules.add_rule(ImportUploadInfo())
        return adapter

    @request_property
    def form_schema(self):

        form_schema = EditNode.form_schema(self)

        form_schema.add_member(
            FileUpload("upload",
                async = True,
                async_uploader = async_uploader,
                async_upload_url = "/async_upload",
                hash_algorithm = "md5",
                get_file_destination = lambda upload: self.temp_file_path,
                member_group = "content",
                required =
                    not (self.item.is_inserted and self.item.file_name)
            )
        )

        return form_schema

    def iter_changes(self, source = None):

        for member, language in EditNode.iter_changes(self, source):

            # Ignore differences on the upload field if no file has been
            # uploaded
            if member.name == "upload":
                upload = schema.get(self.form_data, "upload", None)
                if (
                    upload is None
                    or upload.get("file_hash") == self.item.file_hash
                ):
                    continue

            yield (member, language)

    @property
    def temp_file_path(self):
        return app.path("upload", "temp", "%s-%s-%s" % (
            self.item_id,
            session.id,
            self.stack.to_param()
        ))

    @event_handler
    def handle_saving(cls, event):

        # Move the uploaded file to its permanent location
        stack_node = event.source
        src = stack_node.temp_file_path

        if os.path.exists(src):

            dest = stack_node.item.file_path

            if os.path.exists(dest):
                os.remove(dest)

            move(src, dest)

        stack_node.form_data["upload"] = None


class ImportUploadInfo(schema.Rule):

    def adapt_object(self, context):

        context.consume("upload")
        upload = context.get("upload", None)

        if upload:
            context.set("file_name", schema.get(upload, "file_name"))
            context.set("mime_type", schema.get(upload, "mime_type"))
            context.set("file_size", schema.get(upload, "file_size"))
            context.set("file_hash", schema.get(upload, "file_hash"))


class FileRequiredError(ValidationError):

    @property
    def invalid_members(self):
        return self.member["upload"]

