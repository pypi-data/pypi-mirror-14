#-*- coding: utf-8 -*-
"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2009
"""
from simplejson import dumps
from cocktail.translations import translations, get_language
from cocktail.events import Event
from woost import app
from woost.models import (
    Extension,
    extension_translations,
    Configuration,
    Publishable
)

translations.define("GoogleAnalyticsExtension",
    ca = u"Google Analytics",
    es = u"Google Analytics",
    en = u"Google Analytics"
)

translations.define("GoogleAnalyticsExtension-plural",
    ca = u"Google Analytics",
    es = u"Google Analytics",
    en = u"Google Analytics"
)

translations.define("GoogleAnalyticsExtension.account",
    ca = u"Compte",
    es = u"Cuenta",
    en = u"Account"
)


class GoogleAnalyticsExtension(Extension):

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Integra el lloc web amb Google Analytics.""",
            "ca"
        )
        self.set("description",
            u"""Integra el sitio web con Google Analytics.""",
            "es"
        )
        self.set("description",
            u"""Integrates the site with Google Analytics.""",
            "en"
        )

    def _load(self):

        from woost.extensions.googleanalytics import (
            strings,
            configuration,
            website,
            document,
            block,
            element,
            eventredirection,
            customdefinition
        )

        # Install an overlay to generate events for links pointing to
        # publishable elements
        from cocktail.html import templates
        templates.get_class("woost.extensions.googleanalytics.BaseViewOverlay")
        templates.get_class("woost.extensions.googleanalytics.LinkOverlay")
        templates.get_class("woost.extensions.googleanalytics.TextBlockViewOverlay")
        templates.get_class("woost.extensions.googleanalytics.LanguageSelectorOverlay")

        from cocktail.events import when
        from woost.controllers import CMSController

        @when(CMSController.producing_output)
        def handle_producing_output(e):
            publishable = e.output.get("publishable")
            if (
                publishable is None
                or getattr(publishable, "is_ga_tracking_enabled", lambda: True)()
            ):
                html = e.output.get("head_end_html", "")
                if html:
                    html += " "
                html += self.get_analytics_page_hit_script(publishable)
                e.output["head_end_html"] = html

    def _install(self):
        from woost.extensions.googleanalytics import installationstrings
        self._create_default_custom_definitions()

    def _create_default_custom_definitions(self):

        from .customdefinition import GoogleAnalyticsCustomDefinition

        Configuration.instance.google_analytics_custom_definitions.extend([
            self._create_asset(
                GoogleAnalyticsCustomDefinition,
                "default_custom_definitions.locale",
                title = extension_translations,
                identifier = "woost.locale",
                initialization =
                    "from cocktail.translations import get_language\n"
                    "value = get_language()"
            ),
            self._create_asset(
                GoogleAnalyticsCustomDefinition,
                "default_custom_definitions.roles",
                title = extension_translations,
                identifier = "woost.roles",
                initialization =
                    "from woost import app\n"
                    "value = set(app.user.iter_roles())"
            ),
            self._create_asset(
                GoogleAnalyticsCustomDefinition,
                "default_custom_definitions.path",
                title = extension_translations,
                identifier = "woost.path",
                initialization =
                    "value = reversed(list(publishable.ascend_tree(True)))"
            ),
            self._create_asset(
                GoogleAnalyticsCustomDefinition,
                "default_custom_definitions.publishable",
                title = extension_translations,
                identifier = "woost.publishable",
                initialization =
                    "value = publishable"
            ),
            self._create_asset(
                GoogleAnalyticsCustomDefinition,
                "default_custom_definitions.type",
                title = extension_translations,
                identifier = "woost.type",
                initialization =
                    "from woost.models import Publishable\n"
                    "value = [\n"
                    "   cls\n"
                    "   for cls in publishable.__class__.__mro__\n"
                    "   if cls is not Publishable and issubclass(cls, Publishable)\n"
                    "]"
            )
        ])

    inclusion_code = {
        "async":
            """
            <script type="text/javascript">
              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
              %(create_tracker_command)s
              %(commands)s
            </script>
            """,
        "sync":
            """
            <script type="text/javascript">
              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
              %(create_tracker_command)s;
              ga(function () {
                  %(commands)s
              });
            </script>
            """,
    }

    declaring_tracker = Event()

    def get_analytics_script(self,
        publishable = None,
        commands = None,
        async = True
    ):
        from .utils import get_ga_custom_values

        config = Configuration.instance

        if publishable is None:
            publishable = app.publishable

        event = self.declaring_tracker(
            publishable = publishable,
            account = config.get_setting("google_analytics_account"),
            tracker_parameters = {},
            domain = config.get_setting("google_analytics_domain"),
            template = self.inclusion_code["async" if async else "sync"],
            values = get_ga_custom_values(publishable),
            commands = commands or []
        )

        if not event.account:
            return ""

        commands = event.commands
        parameters = {}

        if event.domain:
            event.tracker_parameters["cookieDomain"] = event.domain

        parameters["create_tracker_command"] = \
            self._serialize_commands([(
                "create",
                event.account,
                event.tracker_parameters
            )])

        if event.values:
            commands.insert(0, ("set", event.values))

        parameters["commands"] = self._serialize_commands(commands)
        return event.template % parameters

    def get_analytics_page_hit_script(self, publishable = None):
        return self.get_analytics_script(
            publishable = publishable,
            commands = [("send", "pageview")]
        )

    def _serialize_commands(self, commands):
        return "\n".join(
            "ga(%s);" % (", ".join(dumps(arg) for arg in cmd))
            for cmd in commands
        )

