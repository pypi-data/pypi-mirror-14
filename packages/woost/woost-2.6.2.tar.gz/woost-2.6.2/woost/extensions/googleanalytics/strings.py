#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

translations.define("Configuration.google_analytics_api",
    ca = u"API de Google Analytics",
    es = u"API de Google Analytics",
    en = u"Google Analytics API"
)

for cls_name in ("Configuration", "Website"):
    translations.define(cls_name + ".services.google_analytics",
        ca = u"Google Analytics",
        es = u"Google Analytics",
        en = u"Google Analytics"
    )

    translations.define(cls_name + ".google_analytics_account",
        ca = u"Compte de Google Analytics",
        es = u"Cuenta de Google Analytics",
        en = u"Google Analytics account"
    )

    translations.define(cls_name + ".google_analytics_domain",
        ca = u"Domini per Google Analytics",
        es = u"Dominio para Google Analytics",
        en = u"Domain for Google Analytics"
    )

translations.define("Document.ga_tracking_enabled",
    ca = u"Habilitar seguiment amb Google Analytics",
    es = u"Habilitar seguimiento con Google Analytics",
    en = u"Track with Google Analytics"
)

# Client redirections
#------------------------------------------------------------------------------
translations.define("woost.extensions.googleanalytics.redirection_title",
    ca = u"Obrint recurs",
    es = u"Abriendo recurso",
    en = u"Downloading resource"
)

translations.define("woost.extensions.googleanalytics.redirection_body",
    ca = lambda url:
        u"S'està obrint el recurs sol·licitat. Si no s'obre automàticament, "
        u"si us plau faci clic <a href='%s'>aquí</a>."
        % url,
    es = lambda url:
        u"Se está abriendo el recurso solicitado. Si no se abre "
        u"automáticamente, por favor haga clic <a href='%s'>aquí</a>."
        % url,
    en = lambda url:
        u"The page or file you requested is being downloaded. If the download "
        u"doesn't start automatically, please click <a href='%s'>here</a>."
        % url
)

