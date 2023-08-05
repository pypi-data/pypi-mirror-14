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
from cocktail.controllers import context
from woost.models import (
    Extension,
    Configuration,
    get_current_user
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
            eventredirection
        )

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

    inclusion_code = {
        "ga.js-async":
            """
            <script type="text/javascript">
                var _gaq = _gaq || [];
                _gaq.push(['_setAccount', '%(account)s']);
                %(commands)s
                (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
                })();
            </script>
            """,
        "ga.js-sync":
            """
            <script type="text/javascript" src="http://www.google-analytics.com/ga.js"></script>
            <script type="text/javascript">
                _gaq.push(['_setAccount', '%(account)s']);
                %(commands)s
            </script>
            """,
        "universal-async":
            """
            <script type="text/javascript">
              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
              ga("create", "%(account)s");
              %(commands)s
            </script>
            """,
        "universal-sync":
            """
            <script type="text/javascript">
              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
              ga("create", "%(account)s");
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
        config = Configuration.instance
        api = config.google_analytics_api
        classic_api = (api == "ga.js")

        if publishable is None:
            publishable = context.get("publishable")

        event = self.declaring_tracker(
            api = api,
            publishable = publishable,
            account = config.get_setting("google_analytics_account"),
            template =
                self.inclusion_code[api + ("-async" if async else "-sync")],
            values =
                None if classic_api else self.get_analytics_values(publishable),
            commands = commands or []
        )

        parameters = {"account": event.account}

        if classic_api:
            parameters["commands"] = \
                self._serialize_ga_commands(event.commands)
        else:
            commands = event.commands

            if event.values:
                commands.insert(0, ("set", event.values))

            parameters["commands"] = \
                self._serialize_universal_commands(commands)

        return event.template % parameters

    def get_analytics_page_hit_script(self, publishable = None):

        api = Configuration.instance.google_analytics_api

        if api == "ga.js":
            commands = [("_trackPageview",)]
        elif api == "universal":
            commands = [("send", "pageview")]
        else:
            return ""

        return self.get_analytics_script(
            publishable = publishable,
            commands = commands
        )

    def get_analytics_values(self, publishable):
        return {
            # Custom dimension: language
            "dimension1": get_language() or "",

            # Custom dimension: roles
            "dimension2":
                self.serialize_collection(
                    role.id for role in get_current_user().iter_roles()
                ),

            # Custom dimension: path
            "dimension3":
                "" if publishable is None
                else self.serialize_collection(
                    ancestor.id
                    for ancestor
                    in reversed(list(publishable.ascend_tree(True)))
                )
        }

    def serialize_collection(self, value):
        return "-" + "-".join(str(item) for item in value) + "-"

    def _serialize_ga_commands(self, commands):
        return "\n".join(
            "_gaq.push([%s]);" % (", ".join(dumps(arg) for arg in cmd))
            for cmd in commands
        )

    def _serialize_universal_commands(self, commands):
        return "\n".join(
            "ga(%s);" % (", ".join(dumps(arg) for arg in cmd))
            for cmd in commands
        )

