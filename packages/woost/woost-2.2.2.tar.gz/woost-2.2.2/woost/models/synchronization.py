#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import re
from decimal import Decimal
from fractions import Fraction
from simplejson import dumps, loads
import urllib2
import datetime
import hashlib
import base64
from BTrees.OOBTree import OOBTree
from cocktail.events import when
from cocktail.modeling import (
    ListWrapper,
    SetWrapper,
    DictWrapper
)
from cocktail.pkgutils import get_full_name, resolve
from cocktail import schema
from cocktail.persistence import datastore
from woost.models.item import Item

RegExp = type(re.compile(""))


class Synchronization(object):

    date_format = "%Y-%m-%d"
    time_format = "%H:%M:%S"
    datetime_format = date_format + " " + time_format

    def __init__(self,
        remote_installation_url = None,
        remote_user = None,
        remote_password = None
    ):
        self.__local_copies = {}
        self.remote_installation_url = remote_installation_url
        self.remote_user = remote_user
        self.remote_password = remote_password

    def get_local_copy(self, global_id):
        return (
            self.__local_copies.get(global_id)
            or Item.get_instance(global_id = global_id)
        )

    def process_manifest(self):
        manifest = get_manifest()
        for global_id, object_hash in manifest.iteritems():
            if object_hash is None:
                obj = Item.require_instance(global_id = global_id)
                object_hash = self.get_object_state_hash(obj)
                manifest[global_id] = object_hash
            yield global_id, object_hash

    def get_object_state_hash(self, obj):
        state = self.export_object_state(obj)
        state = self.__stabilize(state)

        try:
            json = dumps(state)
        except Exception, error:
            raise ValueError("Can't serialize %r (%s)" % (
                obj,
                error
            ))

        return hashlib.md5(json).hexdigest()

    def __stabilize(self, data):
        if isinstance(data, dict):
            return [
                [key, self.__stabilize(data[key])]
                for key in sorted(data)
            ]
        elif isinstance(data, list):
            return [self.__stabilize(value) for value in data]
        else:
            return data

    def serialize_object_state(self, obj):
        return dumps(self.export_object_state(obj))

    def export_object_state(self, obj):

        state = {
            "__class__": obj.__class__.full_name
        }

        for key, member in obj.__class__.members().iteritems():
            if member.synchronizable:
                value = self.export_member(obj, member)
                state[key] = value

        return state

    def export_member(self, obj, member):
        if member.translated:
            return dict(
                (lang, self.export_value(obj.get(member, lang)))
                for lang in obj.translations
            )
        elif isinstance(member, schema.Collection):
            return [
                self.export_value(item)
                for item in (obj.get(member) or ())
            ]
        else:
            return self.export_value(obj.get(member))

    def export_value(self, value):
        if isinstance(value, Item):
            return value.global_id
        elif isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        elif isinstance(value, datetime.date):
            return value.strftime(self.date_format)
        elif isinstance(value, datetime.time):
            return value.strftime(self.time_format)
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, Fraction):
            return str(value)
        elif isinstance(value, tuple):
            return [self.export_value(item) for item in value]
        elif isinstance(value, (ListWrapper, SetWrapper, DictWrapper)):
            return self.export_value(value._items)
        elif isinstance(value, RegExp):
            return base64.b64encode(value.pattern)
        elif isinstance(value, schema.SchemaClass):
            return get_full_name(value)
        else:
            return value

    def import_object_state(self, obj, state):

        if isinstance(obj.__class__, schema.Schema):
            obj_schema = obj.__class__
        else:
            obj_schema = resolve(state["__class__"])

        for key, value in state.iteritems():

            if key == "__class__":
                continue

            member = obj_schema.get_member(key)
            if member is None:
                continue

            if member.synchronizable:
                self.import_member(obj, member, value)

    def import_member(self, obj, member, value):
        if member.translated:
            for lang, translated_value in value.iteritems():
                translated_value = self.import_value(member, translated_value)
                schema.set(obj, member, translated_value, lang)
        else:
            value = self.import_value(member, value)
            schema.set(obj, member, value)

    def import_value(self, member, value):

        if value is None:
            return None
        elif isinstance(member, schema.Reference):
            if member.class_family:
                return resolve(value)
            else:
                return self.get_local_copy(value)
        elif isinstance(member, schema.DateTime):
            return datetime.datetime.strptime(value, self.datetime_format)
        elif isinstance(member, schema.Date):
            return datetime.datetime.strptime(value, self.date_format).date()
        elif isinstance(member, schema.Time):
            return datetime.datetime.strptime(value, self.time_format).time()
        elif isinstance(member, schema.Decimal):
            return Decimal(value)
        elif isinstance(member, schema.Fraction):
            return Fraction(value)
        elif isinstance(member, schema.Tuple):
            return tuple(
                self.import_value(submember, subvalue)
                for submember, subvalue in zip(member.items, value)
            )
        elif isinstance(member, schema.Collection):
            return member.default_type([
                self.import_value(member.items, item)
                for item in value
            ])
        elif isinstance(member, schema.RegularExpression):
            return base64.b64decode(value)
        else:
            return value

    def _sync_request(self, action):

        url = (
            self.remote_installation_url.rstrip("/")
            + "/cms/synchronization/"
            + action
        )

        request = urllib2.Request(url)

        # Add authentication headers
        if self.remote_user:
            request.add_header("X-Woost-User", self.remote_user)

        if self.remote_password:
            request.add_header("X-Woost-Password", self.remote_password)

        return urllib2.urlopen(request)

    def download_file(self, file, chunk_size = 1024):
        response = self._sync_request("file/" + file.global_id)
        with open(file.file_path, "wb") as dest:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                dest.write(chunk)

    def compare_manifests(self):

        response = self._sync_request("manifest")

        incomming = set()
        modified = set()
        local_manifest = get_manifest()

        for line in response:
            line = line.strip()
            pos = line.find(" ")
            global_id = line[:pos]
            remote_hash = line[pos + 1:].strip()
            local_obj = Item.get_instance(global_id = global_id)

            if local_obj is None:
                incomming.add(global_id)
            else:
                local_hash = local_manifest.get(global_id)
                if local_hash is None:
                    local_hash = self.get_object_state_hash(local_obj)
                    local_manifest[global_id] = local_hash
                if remote_hash != local_hash:
                    modified.add(global_id)

        return {"incomming": incomming, "modified": modified}

    def compare_content(self, establish_relations = False):

        self.__local_copies.clear()

        # Find incomming / outgoing / modified items
        manifest_diff = self.compare_manifests()

        # Retrieve the state for remotely added/modified objects
        remote_ids = (manifest_diff["incomming"]  | manifest_diff["modified"])
        changes = {}

        if remote_ids:
            response = self._sync_request("state/" + ",".join(remote_ids))
            remote_state = loads(response.read())

            # Build a local copy of each object that has been added by the remote
            # installation
            for global_id in manifest_diff["incomming"]:
                state = remote_state[global_id]
                model = resolve(state["__class__"])
                local_copy = model(id = None, global_id = global_id)
                local_copy.bidirectional = establish_relations
                self.__local_copies[global_id] = local_copy

            # Initialize the local copies with the received state
            for global_id in manifest_diff["incomming"]:
                self.import_object_state(
                    self.__local_copies[global_id],
                    remote_state[global_id]
                )

            for global_id in manifest_diff["modified"]:
                local_copy = Item.require_instance(global_id = global_id)
                item_remote_state = {}
                self.import_object_state(
                    item_remote_state,
                    remote_state[global_id],
                )

                changes[global_id] = {
                    "local": local_copy,
                    "remote": item_remote_state,
                    "diff": list(
                        (member, lang)
                        for member, lang in schema.diff(
                            local_copy,
                            item_remote_state,
                            schema = local_copy.__class__
                        )
                        if member.synchronizable
                    )
                }


        return {
            "incomming": self.__local_copies.values(),
            "modified": changes
        }

MANIFEST_KEY = "woost.manifest"
debug = False

def get_manifest():
    manifest = datastore.root.get(MANIFEST_KEY)

    if manifest is None:
        datastore.root[MANIFEST_KEY] = manifest = OOBTree()

    return manifest

def rebuild_manifest(eager = True):
    datastore.root[MANIFEST_KEY] = manifest = OOBTree()

    if eager:
        sync = Synchronization()

    for obj in Item.select(Item.synchronizable.equal(True)):
        global_id = obj.global_id
        if global_id:
            if eager:
                object_hash = sync.get_object_state_hash(obj)
                manifest[global_id] = object_hash
            else:
                manifest[global_id] = None

@when(Item.inserting)
def _insert_into_manifest(e):
    obj = e.source
    if obj.synchronizable:
        global_id = e.source.global_id
        if global_id:
            get_manifest()[global_id] = None
            if debug:
                print styled("Manifest: declared " + obj.global_id, "bright_green")

@when(Item.changed)
def _invalidate_manifest(e):

    from cocktail.styled import styled

    obj = e.source

    if not obj.is_inserted:
        return

    # Elegibility for synchronization changed
    if e.member is Item.synchronizable:

        # Object becomes synchronizable: add it to the manifest
        if e.value:
            if obj.global_id:
                get_manifest()[obj.global_id] = None
                if debug:
                    print styled("Manifest: declared " + obj.global_id, "bright_green")
        # Object ceases to be synchronizable: remove it from the manifest
        else:
            get_manifest().pop(obj.global_id, None)
            if debug:
                print styled("Manifest: removed " + obj.global_id, "magenta")

        return

    elif not obj.synchronizable:
        return

    # Object global identifier changed
    if e.member is Item.global_id:
        manifest = get_manifest()

        if e.previous_value:
            manifest.pop(e.previous_value, None)
            if debug:
                print styled("Manifest: removed " + obj.global_id, "magenta")

        if e.value:
            manifest[e.value] = None
            if debug:
                print styled("Manifest: declared " + obj.global_id, "bright_green")

        return

    elif not obj.global_id:
        return

    # Changing a synchronizable member: invalidate the stored object's hash in
    # the manifest, if any
    if e.member.synchronizable:
        get_manifest()[obj.global_id] = None
        if debug:
            print styled("Manifest: invalidated " + obj.global_id, "cyan")

@when(Item.deleted)
def _remove_from_manifest(e):
    get_manifest().pop(e.source.global_id, None)

