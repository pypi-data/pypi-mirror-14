#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

# Configuration / Website
#------------------------------------------------------------------------------
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

    translations.define(cls_name + ".google_analytics_language",
        ca = u"Idioma pels literals enviats a Google Analytics",
        es = u"Idioma para los literales enviados a Google Analytics",
        en = u"Language of text fragments sent to Google Analytics"
    )

    translations.define(cls_name + ".google_analytics_language-explanation",
        ca = u"Algunes funcionalitats, com ara la generació automàtica "
             u"d'esdeveniments pels clics a blocs de text i imatge, poden "
             u"inserir textos a les estadístiques de Google Analytics (per "
             u"exemple, el nom del bloc on s'ha fet el clic). Aquesta opció "
             u"determina l'idioma que s'hauria d'utilitzar per obtenir "
             u"aquests textos.",
        es = u"Algunas funcionalidades, como la generación automática de "
             u"eventos para los clics en bloques de texto e imagen, pueden "
             u"insertar textos en las estadísticas de Google Analytics (por "
             u"ejemplo, el nombre del bloque donde se ha hecho el clic). Esta "
             u"opción determina el idioma que debería utilizarse para obtener "
             u"estos textos.",
        en = u"Some features, such as the automatic generation of events for "
             u"clicks on text + image blocks, can insert text literals into "
             u"Google Analytics statistics (for example, the name of the "
             u"block that received the click). This option controls the "
             u"language that should be used to obtain those texts."
    )

    translations.define(cls_name + ".google_analytics_custom_definitions",
        ca = u"Definicions personalitzades",
        es = u"Definiciones personalizadas",
        en = u"Custom definitions"
    )

    translations.define(
        cls_name + ".google_analytics_custom_definitions-explanation",
        ca = u"Afegeix dimensions o mètriques personalitzades a les "
             u"estadístiques. Important: s'han de replicar les definicions "
             u"manualment a la configuració de la propietat de Google Analytics,"
             u"en el mateix ordre en que es defineixin aquí.",
        es = u"Añade dimensiones o métricas personalizadas a las estadísticas. "
             u"Importante: las definiciones deben replicarse manualmente en la "
             u"configuración de la propiedad de Google Analytics, en el mismo "
             u"orden en que se definan aquí.",
        en = u"Adds custom dimensions or metrics to the page hit / event "
             u"statistics. Important: all definitions must be manually replicated "
             u"on the configuration of the Google Analytics property, in the same "
             u"order they are defined here."
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

# GoogleAnalyticsCustomDefinition
#------------------------------------------------------------------------------
translations.define("GoogleAnalyticsCustomDefinition",
    ca = u"Definició personalitzada de Google Analytics",
    es = u"Definición personalizada de Google Analytics",
    en = u"Custom definition for Google Analytics"
)

translations.define("GoogleAnalyticsCustomDefinition-plural",
    ca = u"Definicions personalitzada de Google Analytics",
    es = u"Definiciones personalizadas de Google Analytics",
    en = u"Custom definitions for Google Analytics"
)

translations.define("GoogleAnalyticsCustomDefinition.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("GoogleAnalyticsCustomDefinition.identifier",
    ca = u"Identificador",
    es = u"Identificador",
    en = u"Identifier"
)

translations.define("GoogleAnalyticsCustomDefinition.definition_type",
    ca = u"Tipus de definició",
    es = u"Tipo de definición",
    en = u"Definition type"
)

translations.define(
    "GoogleAnalyticsCustomDefinition.definition_type=dimension",
    ca = u"Dimensió",
    es = u"Dimensión",
    en = u"Dimension"
)

translations.define(
    "GoogleAnalyticsCustomDefinition.definition_type=metric",
    ca = u"Mètrica",
    es = u"Métrica",
    en = u"Metric"
)

translations.define("GoogleAnalyticsCustomDefinition.enabled",
    ca = u"Activa",
    es = u"Activa",
    en = u"Enabled"
)

translations.define("GoogleAnalyticsCustomDefinition.content_types",
    ca = u"Tipus d'element",
    es = u"Tipos de elemento",
    en = u"Content types"
)

translations.define("GoogleAnalyticsCustomDefinition.initialization",
    ca = u"Inicialització",
    es = u"Inicialización",
    en = u"Initialization"
)

# LanguageSelectorOverlay
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.googleanalytics."
    "LanguageSelectorOverlay.ga_event_category",
    ca = u"selector-idiomes",
    es = u"selector-de-idiomas",
    en = u"language-selector"
)

translations.define(
    "woost.extensions.googleanalytics."
    "LanguageSelectorOverlay.ga_event_action",
    ca = u"seleccionar-idioma",
    es = u"seleccionar-idioma",
    en = u"select-language"
)

