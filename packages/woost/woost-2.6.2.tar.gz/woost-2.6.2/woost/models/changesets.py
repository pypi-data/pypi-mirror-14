#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
"""
from datetime import datetime
from threading import local
from contextlib import contextmanager
from BTrees.IIBTree import IIBTree
from cocktail.modeling import classgetter
from cocktail.events import event_handler
from cocktail import schema
from cocktail.translations import translations
from cocktail.persistence import PersistentObject, datastore

CHANGES_INDEX_KEY = "woost.models.changesets.ChangeSet.changes-index"

@contextmanager
def changeset_context(author = None):
    """A context manager that eases item versioning. All changes performed on
    CMS items within the call to the manager will be tracked and made part of a
    L{ChangeSet}.

    Calls to this manager can be nested. In that case, only the topmost call
    will actually produce a new changeset, other calls will reuse the root
    changeset.

    @param author: The author of the changeset.
    @type author: L{User<woost.models.User>}

    Example:

        >>> with changeset_context(some_user) as changeset:
        >>>     item1.price = 15.0
        >>>     item1.stock = 3
        >>>     item2.price = 5.75
        >>>     item3 = MyItem()
        >>> len(changeset.changes)
        3
        >>> changeset.changes[item3.id].action
        "create"
        >>> item3.author
        some_user
        >>> changeset.changes[item1.id].changed_members
        set(["price", "stock"])
        >>> changeset.changes[item2.id].changed_members
        set(["price"])
        >>> changeset.changes[item2.id].item_state["price"]
        5.75
    """

    changeset = ChangeSet.current

    # Begin a new changeset
    if changeset is None:
        changeset = ChangeSet()
        changeset.author = author
        changeset.begin()
        changeset.insert()

        try:
            yield changeset
        finally:
            changeset.end()

    # Nested call: don't create a new changeset, just reuse the changeset
    # that is already in place
    else:
        if author and author is not changeset.author:
            raise ValueError("A changeset can only have a single author")

        yield changeset


class ChangeSet(PersistentObject):
    """A persistent record of a set of L{changes<Change>} performed on one or
    more CMS items."""

    members_order = "id", "author", "date", "changes"
    indexed = True
    full_text_indexed = True

    changes = schema.Mapping(
        searchable = False,
        get_item_key = lambda change: change.target and change.target.id
    )

    author = schema.Reference(
        required = True,
        type = "woost.models.User",
        search_control = "cocktail.html.DropdownSelector",
        text_search = True
    )

    date = schema.DateTime(
        required = True,
        default = schema.DynamicDefault(datetime.now)
    )

    _thread_data = local()

    @classgetter
    def current(cls):
        return getattr(cls._thread_data, "current", None)

    @classgetter
    def current_author(cls):
        cs = cls.current
        return cs and cs.author

    def begin(self):

        if self.current:
            raise TypeError("Can't begin a new changeset, another changeset "
                "is already in place")

        self._thread_data.current = self

    def end(self):
        try:
            del self._thread_data.current
        except AttributeError:
            raise TypeError("Can't finalize the current changeset, there's no "
                "changeset in place")

    @classmethod
    def extract_searchable_text(cls, extractor):
        PersistentObject.extract_searchable_text(extractor)
        for change in extractor.current.value.changes.itervalues():
            extractor.extract(change.__class__, change)

    @classgetter
    def changes_index(cls):
        try:
            return datastore.root[CHANGES_INDEX_KEY]
        except KeyError:
            index = IIBTree()
            datastore.root[CHANGES_INDEX_KEY] = index
            return index


class Change(PersistentObject):
    """A persistent record of an action performed on a CMS item."""

    indexed = True
    full_text_indexed = True

    changeset = schema.Reference(
        required = True,
        indexed = True,
        type = "woost.models.ChangeSet"
    )

    action = schema.String(
        required = True,
        indexed = True,
        enumeration = ["create", "modify", "delete"]
    )

    target = schema.Reference(
        required = True,
        type = "woost.models.Item",
        indexed = True,
        bidirectional = True
    )

    changed_members = schema.Collection(
        type = set,
        items = schema.String(),
        indexed = True
    )

    item_state = schema.Mapping(
        required = False
    )

    is_explicit_change = schema.Boolean(
        required = True,
        default = False,
        indexed = True
    )

    def get_previous_change(self):
        target = self.target
        if target is not None:
            changes = target.changes
            index = changes.index(self)
            if index > 0:
                return changes[index - 1]

    def diff(self,
        other_change = None,
        diff_schema = None,
        exclude = None,
        language_subset = None
    ):

        if other_change is None:
            other_change = self.get_previous_change()

        if other_change is None:
            raise ValueError(
                "Can't obtain the diff for %r, it has no parent change"
            )

        if diff_schema is None:
            model = self.target.__class__
            adapter = schema.Adapter()
            adapter.exclude([
                member.name
                for member in model.iter_members()
                if not member.visible or not member.versioned
            ])
            diff_schema = adapter.export_schema(model)

        return schema.diff(
            self.item_state,
            other_change.item_state,
            diff_schema,
            exclude = exclude,
            language_subset = language_subset
        )

    def __translate__(self, language, **kwargs):
        return translations(
            "woost.models.changesets.Change description",
            action = self.action,
            target = self.target
        ) or PersistentObject.__translate__(self, language, **kwargs)

    @event_handler
    def handle_changed(cls, e):
        change = e.source
        member = e.member
        value = e.value

        if member is cls.changeset:
            if e.previous_value is not None:
                raise ValueError("Can't move a change between changesets")
            if value is not None and change.is_inserted:
                ChangeSet.changes_index.insert(change.id, value.id)

    @event_handler
    def handle_inserted(cls, e):
        change = e.source
        changeset = change.changeset
        if changeset is not None:
            ChangeSet.changes_index.insert(change.id, changeset.id)

    @event_handler
    def handle_deleting(cls, e):
        try:
            del ChangeSet.changes_index[e.source.id]
        except KeyError:
            pass


class ChangeSetHasChangeExpression(schema.expressions.Expression):

    def __init__(self, target = None, action = None, include_implicit = True):
        self.target = target
        self.action = action
        self.include_implicit = include_implicit

    def op(self, changeset, action):
        for change in changeset.changes.itervalues():
            if (
                # Filter by target
                (
                    self.target is None
                    or (
                        isinstance(change.target, self.target)
                        if isinstance(self.target, type)
                        else change.target is self.target
                    )
                )
                # Filter by action
                and (
                    self.action is None
                    or change.action == self.action
                )
            ):
                return True

        return False

    def resolve_filter(self, query):

        def impl(dataset):

            changes = Change.select()

            # Exclude implicit changes
            if not self.include_implicit:
                changes.add_filter(Change.is_explicit_change.equal(True))

            # Filter by target / target type
            if isinstance(self.target, type):
                changes.add_filter(Change.target.one_of(self.target.select()))
            elif self.target is not None:
                changes.add_filter(Change.target.equal(self.target))

            # Filter by action
            if self.action:
                changes.add_filter(Change.action.equal(self.action))

            # Intersect with the changesets owning the matching changes
            change_index = ChangeSet.changes_index
            subset = set(
                change_index[change_id] for change_id in changes.execute()
            )
            dataset.intersection_update(subset)
            return dataset

        return ((0, 0), impl)

