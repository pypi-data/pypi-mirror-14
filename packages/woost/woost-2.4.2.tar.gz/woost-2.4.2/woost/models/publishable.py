#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
from datetime import datetime
from cocktail.modeling import getter, classgetter
from cocktail.events import event_handler
from cocktail.pkgutils import import_object
from cocktail.translations import (
    translations,
    get_language,
    require_language
)
from cocktail import schema
from cocktail.schema.expressions import Expression
from cocktail.persistence import datastore, MultipleValuesIndex
from cocktail.controllers import (
    make_uri,
    percent_encode_uri,
    Location
)
from cocktail.html.datadisplay import display_factory
from woost import app
from .enabledtranslations import auto_enables_translations
from .localemember import LocaleMember
from .item import Item
from .role import Role
from .usersession import get_current_user
from .websitesession import get_current_website
from .permission import (
    ReadPermission,
    ReadTranslationPermission,
    PermissionExpression
)
from .caching import CachingPolicy

WEBSITE_PUB_INDEX_KEY = "woost.models.Publishable.per_website_publication_index"


@auto_enables_translations
class Publishable(Item):
    """Base class for all site elements suitable for publication."""

    instantiable = False
    cacheable = True
    edit_view = "woost.views.PublishableFieldsView"
    edit_node_class = (
        "woost.controllers.backoffice.enabledtranslationseditnode."
        "EnabledTranslationsEditNode"
    )
    backoffice_heading_view = "woost.views.BackOfficePublishableHeading"

    type_group = "publishable"

    groups_order = [
        "navigation",
        "presentation",
        "presentation.behavior",
        "presentation.format",
        "publication"
    ]

    members_order = [
        "controller",
        "mime_type",
        "resource_type",
        "encoding",
        "parent",
        "path",
        "full_path",
        "hidden",
        "login_page",
        "per_language_publication",
        "enabled",
        "enabled_translations",
        "websites",
        "access_level",
        "start_date",
        "end_date",
        "requires_https",
        "caching_policies"
    ]

    mime_type = schema.String(
        required = True,
        default = "text/html",
        text_search = False,
        format = r"^[^/]+/[^/]+$",
        listed_by_default = False,
        member_group = "presentation.format"
    )

    resource_type = schema.String(
        indexed = True,
        text_search = False,
        editable = False,
        enumeration = (
            "document",
            "image",
            "audio",
            "video",
            "package",
            "html_resource",
            "other"
        ),
        translate_value = lambda value, language = None, **kwargs:
            u"" if not value else translations(
                "woost.models.Publishable.resource_type " + value,
                 language,
                **kwargs
            ),
        listed_by_default = False,
        member_group = "presentation.format"
    )

    encoding = schema.String(
        listed_by_default = False,
        text_search = False,
        default = "utf-8",
        member_group = "presentation.format"
    )

    controller = schema.Reference(
        type = "woost.models.Controller",
        indexed = True,
        bidirectional = True,
        listed_by_default = False,
        member_group = "presentation.behavior"
    )

    def resolve_controller(self):
        if self.controller and self.controller.python_name:
            return import_object(self.controller.python_name)

    parent = schema.Reference(
        type = "woost.models.Document",
        bidirectional = True,
        related_key = "children",
        listed_by_default = False,
        member_group = "navigation"
    )

    path = schema.String(
        max = 1024,
        indexed = True,
        listed_by_default = False,
        text_search = False,
        member_group = "navigation"
    )

    full_path = schema.String(
        indexed = True,
        unique = True,
        editable = False,
        text_search = False,
        listed_by_default = False,
        member_group = "navigation"
    )

    hidden = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "navigation"
    )

    login_page = schema.Reference(
        listed_by_default = False,
        member_group = "navigation"
    )

    per_language_publication = schema.Boolean(
        required = True,
        default = False,
        indexed = True,
        listed_by_default = False,
        member_group = "publication"
    )

    enabled = schema.Boolean(
        required = True,
        default = True,
        indexed = True,
        listed_by_default = False,
        member_group = "publication"
    )

    enabled_translations = schema.Collection(
        items = LocaleMember(),
        default_type = set,
        indexed = True,
        edit_control = "woost.views.EnabledTranslationsSelector",
        listed_by_default = False,
        member_group = "publication"
    )

    websites = schema.Collection(
        items = "woost.models.Website",
        bidirectional = True,
        related_key = "specific_content",
        edit_control = "cocktail.html.CheckList",
        member_group = "publication"
    )

    access_level = schema.Reference(
        type = "woost.models.AccessLevel",
        bidirectional = True,
        indexed = True,
        edit_control = display_factory(
            "cocktail.html.RadioSelector",
            empty_option_displayed = True
        ),
        listed_by_default = False,
        member_group = "publication"
    )

    start_date = schema.DateTime(
        indexed = True,
        listed_by_default = False,
        affects_cache_expiration = True,
        member_group = "publication"
    )

    end_date = schema.DateTime(
        indexed = True,
        min = start_date,
        listed_by_default = False,
        affects_cache_expiration = True,
        member_group = "publication"
    )

    requires_https = schema.Boolean(
        required = True,
        default = False,
        listed_by_default = False,
        member_group = "publication"
    )

    caching_policies = schema.Collection(
        items = schema.Reference(type = CachingPolicy),
        bidirectional = True,
        integral = True,
        related_end = schema.Reference(),
        member_group = "publication"
    )

    def get_effective_caching_policy(self, **context):

        from woost.models import Configuration

        policies = [
            ((-policy.important, 1), policy)
            for policy in self.caching_policies
        ]
        policies.extend(
            ((-policy.important, 2), policy)
            for policy in Configuration.instance.caching_policies
        )
        policies.sort()

        for criteria, policy in policies:
            if policy.applies_to(self, **context):
                return policy

    @event_handler
    def handle_changed(cls, event):

        member = event.member
        publishable = event.source

        if member.name == "path":
            publishable._update_path(publishable.parent, event.value)

        elif member.name == "parent":
            publishable._update_path(event.value, publishable.path)

            # If the parent element is specific to one or more websites, its
            # descendants will automatically share that specificity
            if event.value:
                publishable.websites = list(event.value.websites)
            else:
                publishable.websites = []

        elif member.name == "mime_type":
            if event.value is None:
                publishable.resource_type = None
            else:
                publishable.resource_type = \
                    get_category_from_mime_type(event.value)

    @event_handler
    def handle_related(cls, event):
        if event.member is cls.websites:
            publishable = event.source
            website = event.related_object

            # Update the index
            if publishable.is_inserted and website.is_inserted:
                index = cls.per_website_publication_index
                index.remove(None, publishable.id)
                index.add(website.id, publishable.id)

    @event_handler
    def handle_unrelated(cls, event):
        if event.member is cls.websites:
            publishable = event.source
            website = event.related_object

            index = cls.per_website_publication_index
            index.remove(website.id, publishable.id)

            # Now available to any website
            if publishable.is_inserted and not publishable.websites:
                index.add(None, publishable.id)

    @event_handler
    def handle_inserted(cls, event):
        event.source.__insert_into_per_website_publication_index()

    @event_handler
    def handle_deleted(cls, event):
        cls.per_website_publication_index.remove(None, event.source.id)

    def __insert_into_per_website_publication_index(self):

        index = self.__class__.per_website_publication_index

        # Available to any website
        if not self.websites:
            index.add(None, self.id)

        # Restricted to a subset of websites
        else:
            for website in self.websites:
                if website.is_inserted:
                    index.add(website.id, self.id)

    @classgetter
    def per_website_publication_index(cls):
        """A database index that enumerates content exclusive to one or more
        websites.
        """
        index = datastore.root.get(WEBSITE_PUB_INDEX_KEY)

        if index is None:
            index = datastore.root.get(WEBSITE_PUB_INDEX_KEY)
            if index is None:
                index = MultipleValuesIndex()
                datastore.root[WEBSITE_PUB_INDEX_KEY] = index

        return index

    @event_handler
    def handle_rebuilding_indexes(cls, e):
        cls.rebuild_per_website_publication_index(verbose = e.verbose)

    @classmethod
    def rebuild_per_website_publication_index(cls, verbose = False):
        if verbose:
            print "Rebuilding the Publishable/Website index"
        del datastore.root[WEBSITE_PUB_INDEX_KEY]
        for publishable in cls.select():
            publishable.__insert_into_per_website_publication_index()

    @classgetter
    def per_language_publication_index(cls):
        return datastore.root[WEBSITE_PUB_INDEX_KEY]

    def _update_path(self, parent, path):

        parent_path = parent and parent.full_path

        if parent_path and path:
            self.full_path = parent_path + "/" + path
        else:
            self.full_path = path

    def get_ancestor(self, depth):
        """Obtain one of the item's ancestors, given its depth in the document
        tree.

        @param depth: The depth level of the ancestor to obtain, with 0
            indicating the root of the tree. Negative indices are accepted, and
            they reverse the traversal order (-1 will point to the item itself,
            -2 to its parent, and so on).
        @type depth: int

        @return: The requested ancestor, or None if there is no ancestor with
            the indicated depth.
        @rtype: L{Publishable}
        """
        tree_line = list(self.ascend_tree(include_self = True))
        tree_line.reverse()
        try:
            return tree_line[depth]
        except IndexError:
            return None

    def ascend_tree(self, include_self = False):
        """Iterate over the item's ancestors, moving towards the root of the
        document tree.

        @param include_self: Indicates if the object itself should be included
            in the iteration.
        @type include_self: bool

        @return: An iterable sequence of pages.
        @rtype: L{Document} iterable sequence
        """
        publishable = self if include_self else self.parent
        while publishable is not None:
            yield publishable
            publishable = publishable.parent

    def descend_tree(self, include_self = False):
        """Iterate over the item's descendants.

        @param include_self: Indicates if the object itself should be included
            in the iteration.
        @type include_self: bool

        @return: An iterable sequence of publishable elements.
        @rtype: L{Publishable} iterable sequence
        """
        if include_self:
            yield self

    def descends_from(self, page):
        """Indicates if the object descends from the given document.

        @param page: The hypothetical ancestor of the page.
        @type page: L{Document<woost.models.document.Document>}

        @return: True if the object is contained inside the given document or
            one of its descendants, or if it *is* the given document. False in
            any other case.
        @rtype: bool
        """
        ancestor = self

        while ancestor is not None:
            if ancestor is page:
                return True
            ancestor = ancestor.parent

        return False

    def is_home_page(self):
        """Indicates if the object is the home page for any website.
        @rtype: bool
        """
        from woost.models import Website
        return bool(self.get(Website.home.related_end))

    def is_internal_content(self, language = None):
        """Indicates if the object represents content from this site.
        @rtype: bool
        """
        return True

    def is_current(self):
        now = datetime.now()
        return (self.start_date is None or self.start_date <= now) \
            and (self.end_date is None or self.end_date > now)

    def is_published(self, language = None, website = None):

        if self.per_language_publication:

            language = require_language(language)
            if language not in self.enabled_translations:
                return False

            from woost.models import Configuration
            if not Configuration.instance.language_is_enabled(language):
                return False

        elif not self.enabled:
            return False

        if not self.is_current():
            return False

        websites_subset = self.websites
        if websites_subset and website != "any":
            if website is None:
                website = get_current_website()
            if website is None or website not in websites_subset:
                return False

        return True

    def is_accessible(self, user = None, language = None, website = None):

        if user is None:
            user = get_current_user()

        return (
            self.is_published(language, website)
            and user.has_permission(
                ReadPermission,
                target = self
            )
            and (
                not self.per_language_publication
                or user.has_permission(
                    ReadTranslationPermission,
                    language = require_language(language)
                )
            )
        )

    @classmethod
    def select_published(cls, *args, **kwargs):
        return cls.select(filters = [
            IsPublishedExpression()
        ]).select(*args, **kwargs)

    @classmethod
    def select_accessible(cls, *args, **kwargs):
        return cls.select(filters = [
            IsAccessibleExpression(get_current_user())
        ]).select(*args, **kwargs)

    def get_uri(self,
        path = None,
        parameters = None,
        language = None,
        host = None,
        encode = True):

        uri = app.url_resolver.get_path(self, language = language)

        if uri is not None:
            if self.per_language_publication:
                uri = app.language.translate_uri(
                    path = uri,
                    language = require_language(language)
                )

            if path:
                uri = make_uri(uri, *path)

            if parameters:
                uri = make_uri(uri, **parameters)

            if host == "?":
                websites = self.websites
                if websites and get_current_website() not in websites:
                    host = websites[0].hosts[0]
                else:
                    host = None
            elif host == "!":
                if self.websites:
                    host = self.websites[0].hosts[0]
                else:
                    from woost.models import Configuration
                    website = (
                        get_current_website()
                        or Configuration.instance.websites[0]
                    )
                    host = website.hosts[0]

            uri = self._fix_uri(uri, host, encode)

        return uri

    def translate_file_type(self, language = None):

        trans = ""

        mime_type = self.mime_type
        if mime_type:
            trans = translations("mime " + mime_type, language = language)

        if not trans:

            res_type = self.resource_type
            if res_type:
                trans = self.__class__.resource_type.translate_value(
                    res_type,
                    language = language
                )

                if trans and res_type != "other":
                    ext = self.file_extension
                    if ext:
                        trans += " " + ext.upper().lstrip(".")

        return trans

    def get_cache_expiration(self):
        now = datetime.now()

        start = self.start_date
        if start is not None and start > now:
            return start

        end = self.end_date
        if end is not None and end > now:
            return end


Publishable.login_page.type = Publishable
Publishable.related_end = schema.Collection()


class IsPublishedExpression(Expression):
    """An expression that tests if items are published."""

    def eval(self, context, accessor = None):
        return context.is_published()

    def resolve_filter(self, query):

        def impl(dataset):

            per_lang_pub_index = Publishable.per_language_publication.index

            # Exclude disabled items
            enabled_subset = set(per_lang_pub_index.values(key = False))
            enabled_subset.intersection_update(
                Publishable.enabled.index.values(key = True)
            )

            language = get_language()

            from woost.models import Configuration
            if Configuration.instance.language_is_enabled(language):
                enabled_for_current_language = set(
                    Publishable.per_language_publication.index.values(
                        key = True
                    )
                )
                enabled_for_current_language.intersection_update(
                    Publishable.enabled_translations.index.values(
                        key = language
                    )
                )
                enabled_subset.update(enabled_for_current_language)

            dataset.intersection_update(enabled_subset)

            # Exclude content by website:
            if len(Configuration.instance.websites) > 1:

                website = get_current_website()
                per_website_index = Publishable.per_website_publication_index

                # - content that can be published on any website
                website_subset = set(per_website_index.values(key = None))

                # - content that can be published on the active website
                if website:
                    website_subset.update(per_website_index.values(key = website.id))

                dataset.intersection_update(website_subset)

            # Remove items outside their publication window
            now = datetime.now()
            dataset.difference_update(
                Publishable.start_date.index.values(
                    min = Publishable.start_date.get_index_value(now),
                    exclude_min = True
                )
            )
            dataset.difference_update(
                Publishable.end_date.index.values(
                    min = None,
                    exclude_min = True,
                    max = Publishable.end_date.get_index_value(now),
                    exclude_max = True
                )
            )

            return dataset

        return ((-1, 1), impl)


class IsAccessibleExpression(Expression):
    """An expression that tests that items can be accessed by a user.

    The expression checks both the publication state of the item and the
    read permissions for the specified user.

    @ivar user: The user that accesses the items.
    @type user: L{User<woost.models.user.User>}
    """
    def __init__(self, user = None):
        Expression.__init__(self)
        self.user = user

    def eval(self, context, accessor = None):
        return context.is_accessible(user = self.user)

    def resolve_filter(self, query):

        def impl(dataset):
            user = self.user or get_current_user()
            access_expr = PermissionExpression(user, ReadPermission)
            published_expr = IsPublishedExpression()
            dataset = access_expr.resolve_filter(query)[1](dataset)
            dataset = published_expr.resolve_filter(query)[1](dataset)

            if not user.has_permission(
                ReadTranslationPermission,
                language = require_language()
            ):
                dataset.difference_update(
                    Publishable.per_language_publication.index.values(
                        key = True
                    )
                )

            return dataset

        return ((-1, 1), impl)


class UserHasAccessLevelExpression(Expression):
    """An expression used in resolving the restrictions imposed by the
    `Publishable.access_level` member.

    The expression determines wether the indicated user belongs to one or more
    roles that have been authorized to access the access level assigned to the
    evaluated content.

    @ivar user: The user to test; defaults to the active user.
    @type user: L{User<woost.models.user.User>}
    """
    def __init__(self, user = None):
        Expression.__init__(self)
        self.user = user

    def eval(self, context, accessor = None):

        if accessor is None:
            accessor = schema.get_accessor(context)

        access_level = accessor.get(context, "access_level")

        return access_level is None or any(
            (role in access_level.roles_with_access)
            for role in (self.user or get_current_user()).iter_roles()
        )

    def resolve_filter(self, query):

        def impl(dataset):
            user = self.user or get_current_user()
            index = Publishable.access_level.index
            restricted_content = set(index.values(
                min = None,
                exclude_min = True
            ))

            for role in user.iter_roles():
                for access_level in role.access_levels:
                    restricted_content.difference_update(
                        index.values(key = access_level.id)
                    )

            dataset.difference_update(restricted_content)
            return dataset

        return ((-1, 1), impl)

# Create a single instance of the expression, to avoid instantiating it on
# every single permission check
user_has_access_level = UserHasAccessLevelExpression()


mime_type_categories = {}

for category, mime_types in (
    ("text/plain", ("text",)),
    ("html_resource", (
        "text/css",
        "text/javascript",
        "text/ecmascript",
        "application/javascript",
        "application/ecmascript"
    )),
    ("document", (
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.presentation",
        "application/msword",
        "application/msexcel",
        "application/msaccess",
        "application/mspowerpoint",
        "application/mswrite",
        "application/vnd.ms-excel",
        "application/vnd.ms-access",
        "application/vnd.ms-powerpoint",
        "application/vnd.ms-project",
        "application/vnd.ms-works",
        "application/vnd.ms-xpsdocument",
        "application/rtf",
        "application/pdf",
        "application/x-pdf",
        "application/postscript",
        "application/x-latex",
        "application/vnd.oasis.opendocument.database"
    )),
    ("package", (
        "application/zip",
        "application/x-rar-compressed",
        "application/x-tar",
        "application/x-gtar",
        "application/x-gzip",
        "application/x-bzip",
        "application/x-stuffit",
        "vnd.ms-cab-compressed"
    ))
):
    for mime_type in mime_types:
        mime_type_categories[mime_type] = category

def get_category_from_mime_type(mime_type):
    """Obtains the file category that best matches the indicated MIME type.

    @param mime_type: The MIME type to get the category for.
    @type mime_type: str

    @return: A string identifier with the category matching the indicated
        MIME type (one of 'document', 'image', 'audio', 'video', 'package',
        'html_resource' or 'other').
    @rtype: str
    """
    pos = mime_type.find("/")

    if pos != -1:
        prefix = mime_type[:pos]

        if prefix in ("image", "audio", "video"):
            return prefix

    return mime_type_categories.get(mime_type, "other")

