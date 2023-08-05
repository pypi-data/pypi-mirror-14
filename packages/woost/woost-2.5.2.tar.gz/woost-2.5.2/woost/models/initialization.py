#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
from __future__ import with_statement
import sha
from string import letters, digits
from random import choice
from optparse import OptionParser
from cocktail.stringutils import random_string
from cocktail.translations import translations
from cocktail.iteration import first
from cocktail.persistence import (
    datastore,
    mark_all_migrations_as_executed,
    reset_incremental_id
)
from woost import app
from woost.models import (
    changeset_context,
    Item,
    Configuration,
    Website,
    Publishable,
    Document,
    Page,
    TextBlock,
    LoginBlock,
    CustomBlock,
    User,
    Role,
    URI,
    Controller,
    Template,
    Style,
    File,
    UserView,
    Permission,
    ReadPermission,
    CreatePermission,
    ModifyPermission,
    DeletePermission,
    RenderPermission,
    ReadMemberPermission,
    ModifyMemberPermission,
    CreateTranslationPermission,
    InstallationSyncPermission,
    ReadTranslationPermission,
    ModifyTranslationPermission,
    DeleteTranslationPermission,
    ReadHistoryPermission,
    AccessLevel,
    DeleteTrigger,
    CustomTriggerResponse,
    EmailTemplate,
    CachingPolicy,
    Extension,
    Trigger,
    TriggerResponse,
    SiteInstallation,
    VideoPlayerSettings,
    rendering,
    load_extensions
)


class TranslatedValues(object):

    def __init__(self, key = None, **kwargs):
        self.key = key
        self.kwargs = kwargs


class SiteInitializer(object):

    admin_email = "admin@localhost"
    admin_password = ""
    languages = ["en"]
    extensions = []
    hosts = ["localhost"]
    base_id = None

    read_only_types = [
        Style,
        User,
        Template,
        EmailTemplate,
        rendering.Renderer,
        rendering.ImageFactory,
        VideoPlayerSettings
    ]

    restricted_types = [
        Role,
        Controller,
        Permission,
        CachingPolicy,
        SiteInstallation,
        Trigger,
        TriggerResponse,
        UserView,
        Extension
    ]

    read_only_members = [
        "woost.models.publishable.Publishable.mime_type",
        "woost.models.configuration.Configuration.login_page",
        "woost.models.configuration.Configuration.generic_error_page",
        "woost.models.configuration.Configuration.not_found_error_page",
        "woost.models.configuration.Configuration.forbidden_error_page",
        "woost.models.configuration.Configuration.maintenance_page",
        "woost.models.website.Website.login_page",
        "woost.models.website.Website.home",
        "woost.models.website.Website.generic_error_page",
        "woost.models.website.Website.not_found_error_page",
        "woost.models.website.Website.forbidden_error_page",
        "woost.models.website.Website.maintenance_page",
    ]

    restricted_members = [
        "woost.models.item.Item.qname",
        "woost.models.item.Item.global_id",
        "woost.models.item.Item.synchronizable",
        "woost.models.publishable.Publishable.encoding",
        "woost.models.publishable.Publishable.login_page",
        "woost.models.publishable.Publishable.requires_https",
        "woost.models.configuration.Configuration.maintenance_addresses",
        "woost.models.configuration.Configuration.languages",
        "woost.models.configuration.Configuration.published_languages",
        "woost.models.configuration.Configuration.default_language",
        "woost.models.configuration.Configuration.heed_client_language",
        "woost.models.configuration.Configuration.timezone",
        "woost.models.configuration.Configuration.smtp_host",
        "woost.models.configuration.Configuration.smtp_user",
        "woost.models.configuration.Configuration.smtp_password",
        "woost.models.configuration.Configuration.renderers",
        "woost.models.configuration.Configuration.image_factories",
        "woost.models.configuration.Configuration.video_player_settings",
        "woost.models.website.Website.hosts",
        "woost.models.website.Website.https_policy",
        "woost.models.website.Website.https_persistence",
        "woost.models.website.Website.published_languages",
        "woost.models.website.Website.default_language",
        "woost.models.website.Website.heed_client_language",
        "woost.models.block.Block.initialization"
    ]

    image_factories = [
        "default",
        "icon16",
        "icon32",
        "backoffice_thumbnail",
        "backoffice_small_thumbnail",
        "edit_blocks_thumbnail",
        "close_up",
        "default_thumbnail",
    ]

    def main(self):

        parser = OptionParser()
        parser.add_option("-u", "--user", help = "Administrator email")
        parser.add_option("-p", "--password", help = "Administrator password")
        parser.add_option("-l", "--languages",
            help = "Comma separated list of languages")
        parser.add_option("--hostname", help = "Hostname for the website")
        parser.add_option("-e", "--extensions",
            default = "",
            help = "The list of extensions to enable")
        parser.add_option("-b", "--base-id",
            type = int,
            help = "Seed the incremental ID sequence at a non-zero value")
        parser.add_option("-i", "--installation-id",
            default = "DEV",
            help = "A unique prefix for this installation, used to assign "
                   "globally unique identifiers for objects."
        )

        options, args = parser.parse_args()

        self.admin_email = options.user
        self.admin_password = options.password

        if self.admin_email is None:
            self.admin_email = raw_input("Administrator email: ") or "admin@localhost"

        if self.admin_password is None:
            self.admin_password = raw_input("Administrator password: ") \
                or random_string(8)

        if options.hostname:
            self.hosts = [options.hostname]

        languages = options.languages \
            and options.languages.replace(",", " ") \
            or raw_input("Languages: ") or "en"

        self.languages = languages.split()
        self.extensions = options.extensions.split(",")
        self.base_id = options.base_id
        app.installation_id = options.installation_id

        self.initialize()

        print u"Your site has been successfully created. You can start it by " \
              u"executing the 'run.py' script. An administrator account for the " \
              u"content manager interface has been generated, with the " \
              u"following credentials:\n\n" \
              u"\tEmail:     %s\n" \
              u"\tPassword:  %s\n\n" % (self.admin_email, self.admin_password)

    def initialize(self):
        self.reset_database()

        with changeset_context() as changeset:
            self.changeset = changeset
            self.create_content()

        mark_all_migrations_as_executed()
        datastore.commit()

    def reset_database(self):
        datastore.clear()
        datastore.close()

        if self.base_id:
            reset_incremental_id(self.base_id)

    def _create(self, _model, **values):
        instance = _model()

        for key, value in values.iteritems():
            if isinstance(value, TranslatedValues):
                trans_key = "woost.initialization."

                if value.key:
                    trans_key += value.key
                else:
                    qname = values.get("qname")
                    if not qname:
                        raise ValueError(
                            "Can't translate the values for %s without "
                            "giving it a qname or providing an explicit "
                            "translation key"
                            % instance
                        )
                    prefix = "woost."
                    assert qname.startswith(prefix)
                    trans_key += qname[len(prefix):] + "." + key

                for language in self.languages:
                    trans = translations(trans_key, language, **value.kwargs)
                    if trans:
                        instance.set(key, trans, language)
            else:
                setattr(instance, key, value)

        instance.insert()
        return instance

    def create_content(self):

        # Bootstrap: create the site's configuration and administrator user
        self.configuration = self.create_configuration()
        self.administrator = self.create_administrator()

        self.configuration.author = self.administrator
        self.administrator.author = self.administrator

        # From this point, the authorship f or further objects is set
        # automatically through the active changeset
        self.changeset.author = self.administrator

        # Default website
        self.website = self.create_website()
        self.configuration.websites.append(self.website)

        # Roles
        self.anonymous_role = self.create_anonymous_role()
        self.anonymous_user = self.create_anonymous_user()

        self.administrator_role = self.create_administrator_role()
        self.administrator.roles.append(self.administrator_role)

        self.everybody_role = self.create_everybody_role()
        self.authenticated_role = self.create_authenticated_role()
        self.editor_role = self.create_editor_role()

        self.editor_access_level = self.create_editor_access_level()

        # File deletion trigger
        self.file_deletion_trigger = self.create_file_deletion_trigger()
        self.configuration.triggers.append(self.file_deletion_trigger)

        # Templates and controllers
        self.create_controllers()
        self.standard_template = self.create_standard_template()

        # Home page
        self.website.home = self.create_home()

        # Default stylesheets
        self.user_stylesheet = self.create_user_stylesheet()

        # Backoffice
        self.backoffice = self.create_backoffice()

        # Error pages
        self.not_found_error_page = self.create_not_found_error_page()
        self.configuration.not_found_error_page = self.not_found_error_page

        self.forbidden_error_page = self.create_forbidden_error_page()
        self.configuration.forbidden_error_page = self.forbidden_error_page

        # Password change
        self.password_change_page = self.create_password_change_page()
        self.password_change_confirmation_page = \
            self.create_password_change_confirmation_page()
        self.password_change_email_template = \
            self.create_password_change_email_template()

        # Login page
        self.login_page = self.create_login_page()
        self.configuration.login_page = self.login_page

        # User views
        self.page_tree_user_view = self.create_page_tree_user_view()
        self.create_file_gallery_user_view()

        # Renderers
        self.content_renderer = self.create_content_renderer()
        self.icon16_renderer = self.create_icon16_renderer()
        self.icon32_renderer = self.create_icon32_renderer()

        self.configuration.renderers = [
            self.content_renderer,
            self.icon16_renderer,
            self.icon32_renderer
        ]

        # Image factories
        for image_factory_id in self.image_factories:
            key = image_factory_id + "_image_factory"
            method_name = "create_%s_image_factory" % image_factory_id
            method = getattr(self, method_name)
            image_factory = method()
            setattr(self, key, image_factory)
            self.configuration.image_factories.append(image_factory)

        # Extensions
        self.enable_extensions()

    def create_configuration(self):
        return self._create(
            Configuration,
            qname = "woost.configuration",
            secret_key = random_string(10),
            default_language = self.languages[0],
            languages = self.languages,
            backoffice_language =
                first(
                    language
                    for language in self.languages
                    if language in
                        Configuration.backoffice_language.enumeration
                )
        )

    def create_administrator(self):
        return self._create(
            User,
            qname = "woost.administrator",
            email = self.admin_email,
            password = self.admin_password
        )

    def create_website(self):
        return self._create(
            Website,
            site_name = TranslatedValues("website.site_name"),
            hosts = self.hosts
        )

    def create_anonymous_role(self):
        return self._create(
            Role,
            qname = "woost.anonymous",
            implicit = True,
            title = TranslatedValues()
        )

    def create_anonymous_user(self):
        return self._create(
            User,
            qname = "woost.anonymous_user",
            email = "anonymous@localhost",
            roles = [self.anonymous_role],
            anonymous = True
        )

    def create_administrator_role(self):
        return self._create(
            Role,
            qname = "woost.administrators",
            title = TranslatedValues(),
            permissions = [
                self._create(ReadPermission, content_type = Item),
                self._create(CreatePermission, content_type = Item),
                self._create(ModifyPermission, content_type = Item),
                self._create(DeletePermission, content_type = Item),
                self._create(ReadMemberPermission),
                self._create(ModifyMemberPermission),
                self._create(InstallationSyncPermission)
            ]
        )

    def create_everybody_role(self):
        role = self._create(
            Role,
            implicit = True,
            qname = "woost.everybody",
            title = TranslatedValues(),
            permissions = [
                self._create(RenderPermission, content_type = Item),
                self._create(
                    ReadPermission,
                    content_type = Publishable,
                    content_expression =
                        "from woost.models import user_has_access_level\n"
                        "items.add_filter(user_has_access_level)"
                )
            ]
        )

        # Restrict readable members
        if self.restricted_members:
            role.permissions.append(
                self._create(
                    ReadMemberPermission,
                    authorized = False,
                    matching_members = self.restricted_members
                )
            )

        role.permissions.append(self._create(ReadMemberPermission))

        # Restrict modifiable members
        if self.read_only_members:
            role.permissions.append(
                self._create(
                    ModifyMemberPermission,
                    authorized = False,
                    matching_members = self.read_only_members
                )
            )

        role.permissions.append(self._create(ModifyMemberPermission))

        # All languages allowed
        role.permissions.extend([
            self._create(CreateTranslationPermission),
            self._create(ReadTranslationPermission),
            self._create(ModifyTranslationPermission),
            self._create(DeleteTranslationPermission)
        ])

        return role

    def create_authenticated_role(self):
        return self._create(
            Role,
            qname = "woost.authenticated",
            implicit = True,
            title = TranslatedValues()
        )

    def create_editor_role(self):
        role = self._create(
            Role,
            qname = "woost.editors",
            title = TranslatedValues(),
            hidden_content_types = [
                Template,
                Controller,
                Style,
                EmailTemplate
            ]
        )

        # Restrict readable types
        if self.restricted_types:
            for restricted_type in self.restricted_types:
                for permission_type in (
                    ReadPermission,
                    CreatePermission,
                    ModifyPermission,
                    DeletePermission
                ):
                    role.permissions.append(
                        self._create(
                            permission_type,
                            authorized = False,
                            content_type = restricted_type
                        )
                    )

        # Restrict modifiable types
        if self.read_only_types:
            for read_only_type in self.read_only_types:
                for permission_type in (
                    CreatePermission,
                    ModifyPermission,
                    DeletePermission
                ):
                    role.permissions.append(
                        self._create(
                            permission_type,
                            authorized = False,
                            content_type = read_only_type
                        )
                    )

        for permission_type in (
            ReadPermission,
            CreatePermission,
            ModifyPermission,
            DeletePermission,
            ReadHistoryPermission
        ):
            role.permissions.append(
                self._create(
                    permission_type,
                    content_type = Item
                )
            )

        role.permissions.append(
            self._create(
                InstallationSyncPermission,
                authorized = False
            )
        )

        return role

    def create_editor_access_level(self):
        return self._create(
            AccessLevel,
            qname = "woost.editor_access_level",
            roles_with_access = [self.editor_role]
        )

    def create_file_deletion_trigger(self):
        return self._create(
            DeleteTrigger,
            qname = "woost.file_deletion_trigger",
            title = TranslatedValues(),
            execution_point = "after",
            batch_execution = True,
            content_type = File,
            responses = [
                self._create(
                    CustomTriggerResponse,
                    code = u"from os import remove\n"
                           u"for item in items:\n"
                           u"    remove(item.file_path)"
                )
            ]
        )

    def create_controllers(self):
        for controller_name in (
            "Document",
            "File",
            "URI",
            "Styles",
            "Feed",
            "BackOffice",
            "FirstChildRedirection",
            "Login",
            "PasswordChange",
            "PasswordChangeConfirmation"
        ):
            controller = self._create(
                Controller,
                qname = "woost.%s_controller" % controller_name.lower(),
                title = TranslatedValues(),
                python_name = "woost.controllers.%scontroller.%sController" % (
                    controller_name.lower(),
                    controller_name
                )
            )
            setattr(self, controller_name.lower() + "_controller", controller)

        # The backoffice controller is placed at an irregular location
        self.backoffice_controller.python_name = (
            "woost.controllers.backoffice.backofficecontroller."
            "BackOfficeController"
        )

        # Prevent anonymous access to the backoffice controller
        self._create(
            ReadPermission,
            role = self.anonymous_role,
            content_type = Publishable,
            content_expression =
                """items.add_filter(cls.qname.equal("woost.backoffice"))""",
            authorized = False
        )

    def create_standard_template(self):
        return self._create(
            Template,
            qname = "woost.standard_template",
            title = TranslatedValues(),
            identifier = "woost.views.GenericSiteLayout",
        )

    def create_home(self):
        return self._create(
            Page,
            title = TranslatedValues("home.title"),
            inner_title = TranslatedValues("home.inner_title"),
            blocks = [
                self._create(
                    TextBlock,
                    text = TranslatedValues("home.body")
                )
            ]
        )

    def create_user_stylesheet(self):
        return self._create(
            Document,
            qname = "woost.user_styles",
            title = TranslatedValues(),
            per_language_publication = False,
            controller = self.styles_controller,
            path = "user_styles",
            hidden = True,
            mime_type = "text/css",
            caching_policies = [
                self._create(
                    CachingPolicy,
                    cache_tags_expression =
                        "tags.add('woost.models.style.Style')\n",
                    server_side_cache = True
                )
            ]
        )

    def create_backoffice(self):
        return self._create(
            Document,
            qname = "woost.backoffice",
            title = TranslatedValues(),
            hidden = True,
            path = "cms",
            per_language_publication = False,
            controller = self.backoffice_controller
        )

    def create_not_found_error_page(self):
        return self._create(
            Page,
            qname = "woost.not_found_error_page",
            title = TranslatedValues(),
            hidden = True,
            blocks = [
                self._create(
                    TextBlock,
                    text = TranslatedValues("not_found_error_page.body")
                )
            ]
        )

    def create_forbidden_error_page(self):
        return self._create(
            Page,
            qname = "woost.forbidden_error_page",
            title = TranslatedValues(),
            hidden = True,
            blocks = [
                self._create(
                    TextBlock,
                    text = TranslatedValues("forbidden_error_page.body")
                )
            ]
        )

    def create_password_change_page(self):
        return self._create(
            Page,
            qname = "woost.password_change_page",
            title = TranslatedValues(),
            controller = self.passwordchange_controller,
            hidden = True,
            blocks = [
                self._create(
                    TextBlock,
                    text = TranslatedValues("password_change_page.body")
                ),
                self._create(
                    CustomBlock,
                    heading = TranslatedValues("password_change_page.form_title"),
                    view_class = "woost.views.PasswordChangeRequestForm",
                    controller =
                        "woost.controllers.passwordchangecontroller."
                        "PasswordChangeBlockController"
                )
            ]
        )

    def create_password_change_confirmation_page(self):
        return self._create(
            Page,
            qname = "woost.password_change_confirmation_page",
            title = TranslatedValues(),
            controller = self.passwordchangeconfirmation_controller,
            hidden = True,
            blocks = [
                self._create(
                    TextBlock,
                    text = TranslatedValues("password_change_confirmation_page.body")
                ),
                self._create(
                    CustomBlock,
                    heading = TranslatedValues(
                        "password_change_confirmation_page.form_title"
                    ),
                    view_class = "woost.views.PasswordChangeConfirmationForm",
                    controller =
                        "woost.controllers.passwordchangecontroller."
                        "PasswordChangeConfirmationBlockController"
                )
            ]
        )

    def create_password_change_email_template(self):
        return self._create(
            EmailTemplate,
            qname = "woost.password_change_email_template",
            title = TranslatedValues(),
            subject = TranslatedValues(),
            body = TranslatedValues(),
            sender = u'u"noreply@' + self.hosts[0] + '"',
            receivers = u"[user.email]"
        )

    def create_login_page(self):
        return self._create(
            Page,
            qname = "woost.login_page",
            title = TranslatedValues(),
            hidden = True,
            controller = self.login_controller,
            blocks = [
                self._create(LoginBlock)
            ]
        )

    def create_page_tree_user_view(self):
        return self._create(
            UserView,
            qname = "woost.page_tree_user_view",
            title = TranslatedValues(),
            roles = [self.everybody_role],
            parameters = {
                "type": "woost.models.publishable.Publishable",
                "content_view": "tree",
                "filter": None,
                "members": None
            }
        )

    def create_file_gallery_user_view(self):
        return self._create(
            UserView,
            qname = "woost.file_gallery_user_view",
            title = TranslatedValues(),
            roles = [self.everybody_role],
            parameters = {
                "type": "woost.models.file.File",
                "content_view": "thumbnails",
                "filter": None,
                "order": None,
                "members": None
            }
        )

    def create_content_renderer(self):
        return self._create(
            rendering.ChainRenderer,
            qname = "woost.content_renderer",
            title = TranslatedValues(),
            renderers = [
                self._create(rendering.ImageFileRenderer),
                self._create(rendering.PDFRenderer),
                self._create(rendering.VideoFileRenderer),
                self._create(rendering.ImageURIRenderer)
            ]
        )

    def create_icon16_renderer(self):
        return self._create(
            rendering.IconRenderer,
            qname = "woost.icon16_renderer",
            title = TranslatedValues(),
            icon_size = 16
        )

    def create_icon32_renderer(self):
        return self._create(
            rendering.IconRenderer,
            qname = "woost.icon32_renderer",
            title = TranslatedValues(),
            icon_size = 32
        )

    def create_default_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.default_image_factory",
            title = TranslatedValues(),
            identifier = "default"
        )

    def create_icon16_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.icon16_image_factory",
            title = TranslatedValues(),
            identifier = "icon16",
            renderer = self.icon16_renderer,
            applicable_to_blocks = False
        )

    def create_icon32_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.icon32_image_factory",
            title = TranslatedValues(),
            identifier = "icon32",
            renderer = self.icon32_renderer,
            applicable_to_blocks = False
        )

    def create_backoffice_thumbnail_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.backoffice_thumbnail_image_factory",
            title = TranslatedValues(),
            identifier = "backoffice_thumbnail",
            effects = [
                self._create(
                    rendering.Thumbnail,
                    width = "100",
                    height = "100"
                ),
                self._create(
                    rendering.Frame,
                    edge_width = 1,
                    edge_color = "ddd",
                    vertical_padding = "4",
                    horizontal_padding = "4",
                    background = "eee"
                )
            ],
            fallback = self.icon32_image_factory,
            applicable_to_blocks = False
        )

    def create_backoffice_small_thumbnail_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.backoffice_small_thumbnail_image_factory",
            title = TranslatedValues(),
            identifier = "backoffice_small_thumbnail",
            effects = [
                self._create(
                    rendering.Thumbnail,
                    width = "32",
                    height = "32"
                )
            ],
            fallback = self.icon16_image_factory,
            applicable_to_blocks = False
        )

    def create_edit_blocks_thumbnail_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.edit_blocks_thumbnail_image_factory",
            title = TranslatedValues(),
            identifier = "edit_blocks_thumbnail",
            effects = [
                self._create(
                    rendering.Thumbnail,
                    width = "75",
                    height = "75"
                ),
                self._create(
                    rendering.Frame,
                    edge_width = 1,
                    edge_color = "ccc",
                    vertical_padding = "4",
                    horizontal_padding = "4",
                    background = "eee"
                )
            ],
            applicable_to_blocks = False
        )

    def create_close_up_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.close_up_image_factory",
            title = TranslatedValues(),
            identifier = "image_gallery_close_up",
            effects = [
                self._create(
                    rendering.Fill,
                    width = "900",
                    height = "700",
                    preserve_vertical_images = True
                )
            ]
        )

    def create_default_thumbnail_image_factory(self):
        return self._create(
            rendering.ImageFactory,
            qname = "woost.default_thumbnail_image_factory",
            title = TranslatedValues(),
            identifier = "image_gallery_thumbnail",
            effects = [
                self._create(
                    rendering.Fill,
                    width = "200",
                    height = "150",
                    preserve_vertical_images = True
                )
            ]
        )

    def enable_extensions(self):
        # Enable the selected extensions
        if self.extensions:
            load_extensions()
            for extension in Extension.select():
                ext_name = extension.__class__.__name__[:-len("Extension")].lower()
                if ext_name in self.extensions:
                    extension.enabled = True

