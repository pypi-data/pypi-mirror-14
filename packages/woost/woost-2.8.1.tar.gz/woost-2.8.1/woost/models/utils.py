#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import collections
import os
import shutil
import re
from collections import Sequence, Set
from difflib import SequenceMatcher
from ZODB.broken import Broken
from cocktail.styled import styled
from cocktail.modeling import ListWrapper, SetWrapper
from cocktail import schema
from cocktail.translations import get_language, translations
from cocktail import schema
from cocktail.schema.expressions import Self
from cocktail.persistence import (
    datastore,
    Query,
    PersistentObject,
    PersistentClass,
    reset_incremental_id,
    incremental_id
)
from cocktail.persistence.utils import (
    is_broken,
    remove_broken_type as cocktail_remove_broken_type
)
from woost import app
from .item import Item
from .configuration import Configuration
from .permission import ContentPermission
from .changesets import Change
from .role import Role
from .file import File
from . import staticpublication
from . import objectio


def remove_broken_type(
    full_name,
    existing_bases = (),
    relations = (),
    excluded_relations = None,
    languages = None
):
    if languages is None:
        languages = Configuration.instance.languages

    if excluded_relations is None:
        excluded_relations = (Change.target,)

    cocktail_remove_broken_type(
        full_name,
        existing_bases = existing_bases,
        relations = relations,
        excluded_relations = excluded_relations,
        languages = languages
    )

    for role in Role.select():
        for cls in list(role.hidden_content_types):
            if (
                issubclass(cls, Broken)
                and cls.__module__ + "." + cls.__name__ == full_name
            ):
                role.hidden_content_types.remove(cls)

    for permission in ContentPermission.select():
        content_type = permission.content_type
        if content_type.__module__ + "." + content_type.__name__ == full_name:
            permission.delete()

def delete_history():

    for item in Item.select():
        if not is_broken(item):
            try:
                del item._changes
            except AttributeError:
                pass

    for key in list(datastore.root):
        if key.startswith("woost.models.changesets."):
            del datastore.root[key]

def restore_deleted_item(obj):
    if obj.insert():
        for member in obj.__class__.iter_members():
            if (
                isinstance(member, schema.Collection)
                and obj.get(member) is None
            ):
                obj.set(member, member.produce_default(instance = obj))

def iter_text(objects = None):

    if objects is None:
        objects = Item.select()

    for obj in objects:
        for member in obj.__class__.iter_members():
            if isinstance(member, schema.String):
                if member.translated:
                    languages = obj.translations.keys()
                else:
                    languages = (None,)

                for language in languages:
                    value = obj.get(member, language)
                    if value:
                        yield obj, member, language, value

def grep(expr, objects = None):

    if isinstance(expr, basestring):
        expr = re.compile(expr)

    for obj, member, language, value in iter_text(objects):
        matches = list(expr.finditer(value))
        if matches:
            yield obj, member, language, value, matches

def hl(expr, objects = None):

    for obj, member, language, value, matches in grep(expr, objects):
        print styled("-" * 100, style = "bold")
        print styled(repr(obj), style = "bold"),
        print styled(member.name, "slate_blue"),

        if language:
            print styled(language, "pink")
        else:
            print

        hl_value = value
        offset = 0

        for match in matches:
            start, end = match.span()
            original_chunk = value[start:end]
            hl_chunk = styled(original_chunk, "magenta")
            hl_value = (
                hl_value[:start + offset]
                + hl_chunk
                + hl_value[end + offset:]
            )
            offset += len(hl_chunk) - len(original_chunk)

        print hl_value

def replace(expr, replacement, objects = None, mode = "apply"):

    if isinstance(expr, basestring):
        expr = re.compile(expr)

    if mode == "apply":
        apply = True
        show = False
    elif mode == "verbose":
        apply = True
        show = True
    elif mode == "show":
        apply = False
        show = True
    elif mode == "confirm":
        apply = None
        show = True

    for obj, member, language, value in iter_text(objects):
        modified_value = expr.sub(replacement, value)

        if value == modified_value:
            continue

        if show:
            print styled("-" * 100, style = "bold")
            print styled(translations(obj), style = "bold"),
            print styled(member.name, "slate_blue"),

            if language:
                print styled(language, "pink")
            else:
                print

            diff = SequenceMatcher(a = value, b = modified_value)
            chunks = []

            for op, start_a, end_a, start_b, end_b in diff.get_opcodes():
                orig_chunk = value[start_a:end_a]
                new_chunk = modified_value[start_b:end_b]

                if op == "equal":
                    chunks.append(orig_chunk)
                else:
                    if op in ("replace", "delete"):
                        chunks.append(styled(orig_chunk, "white", "red"))

                    if op in ("replace", "insert"):
                        chunks.append(styled(new_chunk, "white", "green"))

            print "".join(chunks)

        if apply is None:
            answer = None
            while answer not in list("yn"):
                answer = raw_input("Replace (y/n)? ")
            if answer == "n":
                continue
        elif not apply:
            continue

        obj.set(member, modified_value, language)

def search(
    query_text,
    objects = None,
    languages = None,
    match_mode = "pattern",
    stemming = None,
    **search_kwargs
):
    if objects is None:
        query = Item.select()
    elif isinstance(objects, (schema.SchemaClass, Query)):
        query = objects.select()
    elif isinstance(objects, collections.Iterable):
        query = Item.select()
        query.base_collection = objects

    if languages is None:
        languages = (None, get_language())

    query.add_filter(
        Self.search(
            query_text,
            languages = languages,
            match_mode = match_mode,
            stemming = stemming,
            **search_kwargs
        )
    )

    if stemming is None:
        stemming = query.type.stemming

    highlighter = schema.SearchHighlighter(
        query_text,
        languages,
        lambda text: styled(text, "magenta"),
        match_mode = match_mode,
        stemming = stemming
    )

    for result in query:
        print styled(result, "slate_blue")
        highlights = highlighter.highlight(result)
        if highlights:
            print highlights

def any_translation(obj, language_chain = None, **kwargs):

    if language_chain is None:
        user = app.user
        language_chain = (
            user
            and user.backoffice_language_chain
            or Configuration.instance.backoffice_language_chain
        )

    if not language_chain:
        return translations(obj, **kwargs)
    else:
        if isinstance(obj, schema.SchemaObject):
            chain_kwargs = kwargs.copy()
            chain_kwargs.setdefault("discard_generic_translation", True)
        else:
            chain_kwargs = kwargs

        for language in language_chain:
            label = translations(
                obj,
                language = language,
                **chain_kwargs
            )
            if label:
                return label
        else:
            return translations(
                obj,
                language = language_chain[0],
                **kwargs
            )

def rebase_id(base_id, verbose = False):

    # Remove all static publication links
    if verbose:
        print "Removing static publication links"

    for file in File.select():
        staticpublication.remove_links(file)

    reset_incremental_id(base_id)
    id_map = {}

    # Change ids in the database
    for root_model in PersistentObject.derived_schemas(recursive = False):
        if root_model.indexed:

            if verbose:
                print "Rebasing", root_model.__name__

            # Rebuild the object map
            pairs = list(root_model.index.items())
            root_model.index = root_model.index.__class__()
            for old_id, obj in pairs:
                id_map[old_id] = new_id = incremental_id()
                obj._id = new_id
                if verbose:
                    print "\t", old_id, ">", new_id
                root_model.index.add(new_id, obj)

            # Rebuild the .keys set for all models
            for model in root_model.schema_tree():
                if verbose:
                    print "\t", "Rebuilding .keys for", model.__name__
                keys = list(model.keys)
                model.keys.clear()
                for old_id in keys:
                    model.keys.insert(id_map[old_id])

            # Rebuild indexes
            root_model.rebuild_indexes(
                recursive = True,
                verbose = verbose
            )
            root_model.rebuild_full_text_indexes(
                recursive = True,
                verbose = verbose
            )

    if verbose:
        print "Committing transaction"

    datastore.commit()

    # Rename uploaded files
    upload_path = app.path("upload")
    uploads = []
    for file_name in os.listdir(upload_path):
        file_path = os.path.join(upload_path, file_name)
        if os.path.isfile(file_path):
            uploads.append(int(file_name))

    uploads.sort()
    uploads.reverse()

    for old_upload_id in uploads:
        new_upload_id = id_map[old_upload_id]
        old_path = os.path.join(upload_path, str(old_upload_id))
        new_path = os.path.join(upload_path, str(new_upload_id))
        if verbose:
            print "Moving upload %s to %s" % (old_path, new_path)
        shutil.move(old_path, new_path)

    # Recreate static publication links
    if verbose:
        print "Creating static publication links"

    for file in File.select():
        staticpublication.create_links(file)

def show_translation_coverage(
    objects = None,
    languages = None,
    styles = (
        (100, {'foreground': 'bright_green'}),
        (90,  {'foreground': 'yellow'}),
        (66,  {'foreground': 'brown'}),
        (33,  {'foreground': 'pink'}),
        (0,   {'foreground': 'magenta'})
    )
):
    count = collections.Counter()

    if objects is None:
        translated_models = {}

        def model_is_translated(model):
            try:
                return translated_models[model]
            except KeyError:
                for member in model.iter_members():
                    if (
                        member is not Item.last_translation_update_time
                        and member.translated
                    ):
                        translated = True
                        break
                    else:
                        translated = False
                translated_models[model] = translated
                return translated

        objects = (
            item
            for item in Item.select()
            if model_is_translated(item.__class__)
        )
    elif isinstance(objects, PersistentClass):
        objects = objects.select()

    if languages is None:
        languages = Configuration.instance.languages

    for lang in languages:
        count[lang] = 0

    for obj in objects:
        for lang in languages:
            if lang in obj.translations:
                count[lang] += 1

    results = count.most_common()
    total = results[0][1]
    table = []
    longest_label_length = 0

    for lang, n in results:
        label = translations("locale", locale = lang)
        longest_label_length = max(longest_label_length, len(label))
        percent = float(n) / total * 100
        table.append((label, percent))

    for label, percent in table:

        line = (
            (label + ":").ljust(longest_label_length + 1)
            + " "
            + ("%.2f%%" % percent).rjust(7)
        )

        if styles:
            for threshold, style in styles:
                if percent >= threshold:
                    line = styled(line, **style)
                    break

        print line

def export_json(
    obj,
    exporter = None,
    json_encoder_settings = None,
    **kwargs
):
    kwargs.setdefault("verbose", True)

    exporter = exporter or objectio.ObjectExporter()
    for key, value in kwargs.iteritems():
        setattr(exporter, key, value)

    if json_encoder_settings is None:
        json_encoder_settings = {"indent": 2, "sort_keys": True}

    if isinstance(obj, (Sequence, Set, ListWrapper, SetWrapper)):
        exporter.add_all(obj)
    elif isinstance(obj, PersistentClass):
        exporter.add_all(obj.select())
    else:
        exporter.add(obj)

    json = exporter.dumps(**json_encoder_settings)
    return json

def import_json(json, importer = None, **kwargs):

    kwargs.setdefault(
        "unknown_member_policy",
        objectio.UnknownMemberPolicy.report
    )

    kwargs.setdefault(
        "missing_object_policy",
        objectio.MissingObjectPolicy.report
    )

    kwargs.setdefault("verbose", True)

    importer = importer or objectio.ObjectImporter()
    for key, value in kwargs.iteritems():
        setattr(importer, key, value)

    importer.loads(json)

def copy_to_clipboard(*args, **kwargs):
    import clipboard
    json = export_json(*args, **kwargs)
    clipboard.copy(json.encode("utf-8"))

def paste_from_clipboard(**kwargs):
    import clipboard
    json = clipboard.paste().decode("utf-8")
    import_json(json, **kwargs)

