#-*- coding: utf-8 -*-
u"""Provides the `UploadForm` class, that makes it easy to upload files into
`woost.models.File` objects.

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from tempfile import mkdtemp
from shutil import move, rmtree
from cocktail import schema
from cocktail.controllers import Form, FileUpload, request_property
from woost.models import File
from woost.controllers import async_uploader


class UploadForm(Form):

    default_upload_options = {
        "async": True,
        "async_uploader": async_uploader,
        "async_upload_url": "/async_upload",
        "hash_algorithm": "md5"
    }

    upload_options = {}

    @request_property
    def upload_members(self):
        is_file_ref = (
            lambda member:
                isinstance(member, schema.Reference)
                and issubclass(member.type, File)
        )
        return [member
                for member in self.model.iter_members()
                if is_file_ref(member)
                or (
                    isinstance(member, schema.Collection)
                    and is_file_ref(member.items)
                )]

    @request_property
    def adapter(self):
        adapter = Form.adapter(self)

        for member in self.upload_members:
            key = member.name
            export_rule = self.ExportUploadInfo(self, key)
            adapter.export_rules.add_rule(export_rule)
            adapter.import_rules.add_rule(self.ImportUploadInfo(self, key))

        return adapter

    def get_upload_options(self):
        options = self.default_upload_options.copy()
        options.update(self.upload_options)
        return options

    class ExportUploadInfo(schema.Rule):

        def __init__(self, form, key):
            self.form = form
            self.key = key

        def adapt_schema(self, context):

            if context.consume(self.key):
                source_member = context.source_schema[self.key]

                upload_options = self.form.get_upload_options()
                upload_options["required"] = source_member.required
                upload_options["get_file_destination"] = \
                    self.form.get_temp_path

                target_member = FileUpload(**upload_options)

                if isinstance(source_member, schema.Collection):
                    target_member = schema.Collection(
                        items = target_member,
                        min = source_member.min,
                        max = source_member.max
                    )

                target_member.name = self.key
                target_member.member_group = source_member.member_group
                context.target_schema.add_member(target_member)
                context.member_created(target_member, source_member)

        def adapt_object(self, context):
            if context.consume(self.key):
                value = context.get(self.key)
                if value:
                    source_member = context.source_schema[self.key]
                    if isinstance(source_member, schema.Collection):
                        adapted_value = [
                            self.export_upload(context, item)
                            for item in value
                        ]
                    else:
                        adapted_value = self.export_upload(context, value)
                    context.set(self.key, adapted_value)

        def export_upload(self, context, file):
            return {
                "file_name": file.file_name,
                "mime_type": file.mime_type,
                "file_size": file.file_size,
                "file_hash": file.file_hash
            }

    class ImportUploadInfo(schema.Rule):

        def __init__(self, form, key):
            self.form = form
            self.key = key

        def adapt_object(self, context):

            if context.consume(self.key):
                value = context.get(self.key, None)

                if value is not None:
                    source_member = context.source_schema[self.key]

                    if isinstance(source_member, schema.Collection):
                        adapted_value = [
                            self.import_upload(context, upload)
                            for upload in value
                        ]
                    else:
                        adapted_value = self.import_upload(context, value)

                    context.set(self.key, adapted_value)

        def import_upload(self, context, upload):

            member = context.target_schema[self.key]
            file = None

            if not isinstance(member, schema.Collection):
                file = context.target_object.get(self.key)

            if file is None:
                file = self.create_file(context)

            file.file_name = upload["file_name"]
            file.mime_type = upload["mime_type"]
            file.file_size = upload["file_size"]
            file.file_hash = upload["file_hash"]

            self.form.temp_paths[file] = self.form.get_temp_path(upload)

            return file

        def create_file(self, context):
            member = context.target_schema[self.key]
            file_type = member.related_type
            if not issubclass(file_type, File):
                file_type = File
            return file_type()

    def submit(self):
        Form.submit(self)
        self.upload()

    @request_property
    def temp_upload_folder(self):
        return mkdtemp()

    @request_property
    def temp_paths(self):
        return {}

    def get_temp_path(self, upload):
        temp_path = upload.get("temp_path")
        if temp_path is None:
            upload["temp_path"] = temp_path = os.path.join(
                self.temp_upload_folder,
                str(id(upload))
            )
        return temp_path

    def upload(self):

        # Move uploaded files to their permanent location
        try:
            for member in self.upload_members:

                if schema.get(self.data, member) is None:
                    continue

                value = schema.get(self.instance, member)

                if isinstance(member, schema.Collection):
                    files = value
                else:
                    files = (value,)

                for i, file in enumerate(files):
                    temp_file = self.temp_paths[file]

                    if os.path.exists(temp_file):

                        dest = file.file_path

                        if os.path.exists(dest):
                            os.remove(dest)

                        move(temp_file, dest)

        # Remove the temporary folder
        finally:
            rmtree(self.temp_upload_folder)

