#-*- coding: utf-8 -*-
u"""Provides the `FileUploader` class, that makes it easy to upload files into
`woost.models.File` objects using forms.

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import os
from tempfile import mkdtemp
from shutil import move, rmtree
from cocktail import schema
from cocktail.controllers import FileUpload, request_property
from woost.models import File
from woost.controllers import async_uploader


class FileUploader(object):

    properties = {}

    upload_options = {
        "async": True,
        "async_uploader": async_uploader,
        "async_upload_url": "/async_upload"
    }

    def __init__(self,
        receiver,
        members = None,
        upload_options = None,
        properties = None
    ):

        if members is None:
            members = [
                member.name
                for member in receiver.__class__.ordered_members()
                if isinstance(member, schema.RelationMember)
                and member.related_type
                and issubclass(member.related_type, File)
            ]

        self.receiver = receiver
        self.members = members

        self.upload_options = self.upload_options.copy()
        if upload_options:
            self.upload_options.update(upload_options)

        self.properties = self.properties.copy()
        if properties:
            self.properties.update(properties)

    def setup_adapter(self, adapter, member_subset = None):

        for key in (member_subset or self.members):
            adapter.export_rules.add_rule(
                self.ExportUpload(
                    self,
                    self.receiver,
                    key,
                    self.upload_options.copy(),
                    self.properties.copy()
                )
            )
            adapter.import_rules.add_rule(
                self.ImportUpload(
                    self,
                    self.receiver,
                    key
                )
            )

        return adapter

    class ExportUpload(schema.Rule):

        upload_options = None

        def __init__(self,
            uploader,
            receiver,
            key,
            upload_options,
            properties
        ):
            self.uploader = uploader
            self.receiver = receiver
            self.key = key
            self.upload_options = upload_options
            self.properties = properties

        def adapt_schema(self, context):

            if context.consume(self.key):
                source_member = context.source_schema[self.key]
                upload_member = FileUpload(
                    required = source_member.required,
                    hash_algorithm = "md5",
                    get_file_destination = self.uploader.get_temp_path
                )

                for key, value in self.upload_options.iteritems():
                    setattr(upload_member, key, value)

                if isinstance(source_member, schema.Collection):
                    target_member = schema.Collection(
                        items = upload_member,
                        min = source_member.min,
                        max = source_member.max
                    )
                else:
                    target_member = upload_member

                target_member.member_group = source_member.member_group

                for key, value in self.properties.iteritems():
                    setattr(target_member, key, value)

                target_member.name = self.key
                context.target_schema.add_member(target_member)
                context.member_created(target_member, source_member)

        def adapt_object(self, context):
            if context.consume(self.key):
                value = self.receiver.get(self.key)
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

    class ImportUpload(schema.Rule):

        def __init__(self, uploader, receiver, key):
            self.uploader = uploader
            self.receiver = receiver
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

                    self.receiver.set(self.key, adapted_value)

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

            self.uploader.temp_paths[file] = \
                self.uploader.get_temp_path(upload)

            return file

        def create_file(self, context):
            member = context.target_schema[self.key]
            return member.related_type()

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
            for key in self.members:

                member = self.receiver.__class__.get_member(key)
                value = schema.get(self.receiver, member)

                if not value:
                    continue

                if isinstance(member, schema.Collection):
                    files = value
                else:
                    files = (value,)

                for file in files:
                    if not file.is_inserted:
                        file.insert()

                    temp_file = self.temp_paths.get(file)

                    if temp_file and os.path.exists(temp_file):

                        dest = file.file_path

                        if os.path.exists(dest):
                            os.remove(dest)

                        move(temp_file, dest)

        # Remove the temporary folder
        finally:
            rmtree(self.temp_upload_folder)

