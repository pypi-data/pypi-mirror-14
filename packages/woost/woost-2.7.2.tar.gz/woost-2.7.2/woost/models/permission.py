#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2009
"""
from contextlib import contextmanager
from cocktail.modeling import InstrumentedSet
from cocktail.events import when
from cocktail.pkgutils import import_object
from cocktail.translations import translations, get_language
from cocktail import schema
from cocktail.schema.expressions import Expression
from cocktail.persistence import PersistentObject
from woost import app
from .item import Item
from .changesets import ChangeSet, Change
from .messagestyles import permission_doesnt_match_style
from .messagestyles import unauthorized_style


class Permission(Item):

    type_group = "access"
    instantiable = False
    visible_from_root = False

    authorized = schema.Boolean(
        required = True,
        default = True
    )

    role = schema.Reference(
        type = "woost.models.Role",
        bidirectional = True,
        min = 1
    )

    def match(self, **kwargs):
        """Indicates if the permission matches the given context.

        @return: True if the permission matches, False otherwise.
        @rtype: bool
        """
        return True

    def __translate__(self, language, **kwargs):
        return translations(
            self.__class__.full_name + "-instance",
            language,
            instance = self,
            **kwargs
        ) or Item.__translate__(self, language, **kwargs)

    @classmethod
    def permission_not_found(cls, user, verbose = False, **context):
        if verbose:
            print unauthorized_style("unauthorized")
        return False


class ContentPermission(Permission):
    """Base class for permissions restricted to a subset of a content type."""

    members_order = [
        "content_type",
        "content_expression",
        "subject_description"
    ]

    content_type = schema.Reference(
        class_family = PersistentObject,
        default = Item,
        required = True
    )

    content_expression = schema.CodeBlock(
        language = "python"
    )

    subject_description = schema.String(
        translated = True,
        spellcheck = True
    )

    def match(self, user, target, verbose = False):

        query = self.select_items(user = user)

        if isinstance(target, type):
            if not issubclass(target, query.type):
                if verbose:
                    print permission_doesnt_match_style("type doesn't match"),
                return False
            elif not self.authorized and self.content_expression:
                if verbose:
                    print permission_doesnt_match_style("partial restriction")
                return False
        else:
            if not issubclass(target.__class__, query.type):
                if verbose:
                    print permission_doesnt_match_style("type doesn't match"),
                return False

            for filter in query.filters:
                if not filter.eval(target):
                    if verbose:
                        print permission_doesnt_match_style(
                            "filter %s doesn't match" % filter
                        ),
                    return False

        return True

    def select_items(self, *args, **kwargs):

        items = self.content_type.select()
        user = kwargs.pop("user", None)

        expression = self.content_expression
        if expression:
            context = {"items": items, "cls": self.content_type, "user": user}
            label = "%s #%s" % (self.__class__.__name__, self.id)
            code = compile(expression, label, "exec")
            exec code in context
            items = context["items"]

        if args or kwargs:
            items = items.select(*args, **kwargs)

        return items


class ReadPermission(ContentPermission):
    """Permission to list and view instances of a content type."""
    instantiable = True


class CreatePermission(ContentPermission):
    """Permission to create new instances of a content type."""
    instantiable = True


class ModifyPermission(ContentPermission):
    """Permission to modify existing instances of a content type."""
    instantiable = True


class DeletePermission(ContentPermission):
    """Permission to delete instances of a content type."""
    instantiable = True


class RenderPermission(ContentPermission):
    """Permission to obtain images representing instances of a content type."""
    instantiable = True

    def _image_factories_enumeration(ctx):
        from woost.models.rendering.factories import image_factories
        return image_factories.keys()

    image_factories = schema.Collection(
        items = schema.String(enumeration = _image_factories_enumeration),
        searchable = False
    )

    del _image_factories_enumeration

    def match(self, user, target, image_factory, verbose = False):

        if self.image_factories and image_factory not in self.image_factories:
            print permission_doesnt_match_style("image_factory doesn't match")
            return False

        return ContentPermission.match(self, user, target, verbose)

    @classmethod
    def permission_not_found(cls, user, verbose = False, **context):
        # If no specific render permission is found, a read permission will do
        return user.has_permission(
            ReadPermission,
            target = context["target"],
            verbose = verbose
        )


class TranslationPermission(Permission):
    """Base class for permissions that restrict operations on languages."""

    def _matching_languages_enumeration(ctx):
        from woost.models import Configuration
        return Configuration.instance.languages

    matching_languages = schema.Collection(
        edit_control = "cocktail.html.CheckList",
        items = schema.String(
            enumeration = _matching_languages_enumeration,
            translate_value = lambda value, language = None, **kwargs:
                u"" if not value else translations(value, language, **kwargs)
        )
    )

    del _matching_languages_enumeration

    def match(self, user, language, verbose = False):

        languages = self.matching_languages

        if languages and language not in languages:
            if verbose:
                print permission_doesnt_match_style("language doesn't match"),
            return False

        return True


class CreateTranslationPermission(TranslationPermission):
    """Permission to add new translations."""
    instantiable = True


class ReadTranslationPermission(TranslationPermission):
    """Permission to view values translated into certain languages."""
    instantiable = True


class ModifyTranslationPermission(TranslationPermission):
    """Permission to modify the values of an existing translation."""
    instantiable = True


class DeleteTranslationPermission(TranslationPermission):
    """Permission to delete translations."""
    instantiable = True

def _resolve_matching_member_reference(compound_name):
    pos = compound_name.rfind(".")
    type_full_name = compound_name[:pos]
    member_name = compound_name[pos+1:]
    cls = import_object(type_full_name)
    return cls[member_name]

def _eligible_members():
    for cls in [Item] + list(Item.derived_schemas()):
        for name, member in cls.members(recursive = False).iteritems():
            if member.visible and member.name != "translations":
                yield cls.full_name + "." + name


def _translate_member_permission_matching_members(
    value,
    language = None,
    **kwargs
):
    if not value:
        return ""

    try:
        member = _resolve_matching_member_reference(value)
    except:
        return "?"
    else:
        return translations(member, language, qualified = True)


class MemberPermission(Permission):
    """Base class for permissions that restrict operations on members."""

    matching_members = schema.Collection(
        default_type = set,
        items = schema.String(
            enumeration = lambda ctx: set(_eligible_members()),
            translate_value = _translate_member_permission_matching_members
        ),
        edit_control = "woost.views.MemberList"
    )

    def match(self, user, member, verbose = False):

        member = member.original_member.schema.full_name + "." + member.name
        members = self.matching_members

        if members and member not in members:
            if verbose:
                print permission_doesnt_match_style("member doesn't match"),
            return False

        return True

    def iter_matching_members(self, ignore_invalid = False):
        for compound_name in self.matching_members:
            try:
                member = _resolve_matching_member_reference(compound_name)
            except:
                if not ignore_invalid:
                    raise
            else:
                yield member


class ReadMemberPermission(MemberPermission):
    """Permission to view the value of certain members."""
    instantiable = True


class ModifyMemberPermission(MemberPermission):
    """Permission to modify the value of certain members."""
    instantiable = True


class ReadHistoryPermission(Permission):
    """Permission to view item revisions."""
    instantiable = True


class InstallationSyncPermission(Permission):
    """Permission to import content from remote installations."""
    instantiable = True


@contextmanager
def restricted_modification_context(
    item,
    user = None,
    member_subset = None,
    verbose = False
):
    """A context manager that restricts modifications to an item.

    @param item: The item to monitor.
    @type item: L{Item<woost.models.item.Item>}

    @param user: The user that performs the modifications. If no user is
        provided, the active user will be used instead.
    @type user: L{User<woost.models.user.User>}

    @param verbose: Set to True to enable debug messages for the permission
        checks executed by this function.
    @type verbose: True

    @raise L{AuthorizationError<woost.models.user.AuthorizationError}:
        Raised if attempting to execute an action on the monitored item without
        the proper permission.
    """
    if user is None:
        user = app.user

    if item.__class__.translated:
        starting_languages = set(item.translations.keys())
        modified_languages = set()

    # Modifying an existing item
    if item.is_inserted:
        is_new = False
        permission_type = ModifyPermission

        # Restrict access *before* the object is modified. This is only done on
        # existing objects, to make sure the current user is allowed to modify
        # them, taking into account constraints that may derive from the
        # object's present state. New objects, by definition, have no present
        # state, so the test is skipped.
        user.require_permission(
            ModifyPermission,
            target = item,
            verbose = verbose
        )

    # Creating a new item
    else:
        is_new = True
        permission_type = CreatePermission

    # Add an event listener to the edited item, to restrict changes to its
    # members
    @when(item.changed)
    def restrict_members(event):

        member = event.member

        # Require permission to modify the changed member
        if member_subset is None or member.name in member_subset:
            user.require_permission(
                ModifyMemberPermission,
                member = member,
                verbose = verbose
            )

        if member.translated:
            language = event.language

            # Require permission to create a new translation
            if is_new:
                if language not in starting_languages \
                and language not in modified_languages:
                    user.require_permission(
                        CreateTranslationPermission,
                        language = language,
                        verbose = verbose
                    )
                    modified_languages.add(language)

            # Require permission to modify an existing translation
            else:
                if language not in modified_languages:
                    user.require_permission(
                        ModifyTranslationPermission,
                        language = language,
                        verbose = verbose
                    )
                    modified_languages.add(language)

    # Try to modify the item
    try:
        yield None

    # Remove the added event listener
    finally:
        item.changed.remove(restrict_members)

    # Require permission to delete removed translations
    if item.__class__.translated:
        for language in starting_languages - set(item.translations):
            user.require_permission(
                DeleteTranslationPermission,
                language = language,
                verbose = verbose
            )

    # Restrict access *after* the object is modified, both for new and old
    # objects, to make sure the user is leaving the object in a state that
    # complies with all existing restrictions.
    user.require_permission(
        permission_type,
        target = item,
        verbose = verbose
    )

def delete_validating(item, user = None, deleted_set = None):

    if user is None:
        user = app.user

    if deleted_set is None:
        class ValidatingDeletedSet(InstrumentedSet):
            def item_added(self, item):
                user.require_permission(DeletePermission, target = item)

        deleted_set = ValidatingDeletedSet()

    item.delete(deleted_set)
    return deleted_set


class PermissionExpression(Expression):
    """An schema expression that indicates if the specified user has permission
    over an element.
    """
    user = None
    permission_type = None

    def __init__(self, user, permission_type):
        self.user = user
        self.permission_type = permission_type

    def eval(self, context, accessor = None):
        return self.user.has_permission(self.permission_type, target = context)

    def resolve_filter(self, query):

        def impl(dataset):

            authorized_subset = set()
            queried_type = query.type
            user = self.user

            for permission in reversed(list(
                user.iter_permissions(self.permission_type)
            )):
                permission_query = permission.select_items(user = user)

                if query.verbose:
                    permission_query.verbose = True
                    permission_query.nesting = query.nesting + 1

                if issubclass(queried_type, permission_query.type) \
                or issubclass(permission_query.type, queried_type):

                    permission_subset = permission_query.execute()

                    if permission.authorized:
                        authorized_subset.update(permission_subset)
                    else:
                        authorized_subset.difference_update(permission_subset)

            dataset.intersection_update(authorized_subset)
            return dataset

        return ((0, 0), impl)


class ChangeSetPermissionExpression(Expression):

    user = None

    def __init__(self, user):
        self.user = user

    def eval(self, context, accessor = None):
        return any(
            self.user.has_permission(
                ReadPermission,
                target = change.target
            )
            for change in context.changes.itervalues()
        )

    def resolve_filter(self, query):

        def impl(dataset):
            authorized_changes = Change.select(
                Change.target.one_of(
                    Item.select(
                        PermissionExpression(self.user, ReadPermission)
                    )
                )
            )
            authorized_changesets = set()
            for change_id in authorized_changes.execute():
                changeset_id = ChangeSet.changes_index[change_id]
                authorized_changesets.add(changeset_id)

            dataset.intersection_update(authorized_changesets)
            return dataset

        return ((0, 0), impl)


class DebugPermission(Permission):
    """Permission to obtain technical details about exceptions and the site's
    internal state.
    """

