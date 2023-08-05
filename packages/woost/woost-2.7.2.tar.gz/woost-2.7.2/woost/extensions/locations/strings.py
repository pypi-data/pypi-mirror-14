#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.iteration import first
from cocktail.translations import translations, get_language
from cocktail.translations.strings \
    import translate_locale_component as base_translate_locale_component
from woost.extensions.locations.location import Location

# Override the translation for locale components to replace country ISO codes
# with human readable descriptions

def translate_locale_component(locale, component, index):

    if index == 1:
        location = first(
            Location.select({
                "location_type": "country",
                "code": component
            })
        )
        if location is not None:
            location_name = translations(
                location,
                discard_generic_translation = True
            )

            if not location_name and get_language() != "en":
                location_name = translations(
                    location,
                    "en",
                    discard_generic_translation = True
                )

            return u" - " + location_name

    return base_translate_locale_component(locale, component, index)

translations.define("locale_component", **dict(
    (lang, translate_locale_component)
    for lang in translations
))

# Location
#------------------------------------------------------------------------------
translations.define("Location",
    ca = u"Ubicació",
    es = u"Ubicación",
    en = u"Location"
)

translations.define("Location-plural",
    ca = u"Ubicacions",
    es = u"Ubicaciones",
    en = u"Locations"
)

translations.define("Location.location_name",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Location.location_type",
    ca = u"Tipus d'ubicació",
    es = u"Tipo de ubicación",
    en = u"Location type"
)

translations.define("woost.extensions.locations.location_types.continent",
    ca = u"Continent",
    es = u"Continente",
    en = u"Continent"
)

translations.define("woost.extensions.locations.location_types.country",
    ca = u"País",
    es = u"País",
    en = u"Country"
)

translations.define(
    "woost.extensions.locations.location_types.autonomous_community",
    ca = u"Comunitat autònoma",
    es = u"Comunidad autónoma",
    en = u"Autonomous community"
)

translations.define(
    "woost.extensions.locations.location_types.province",
    ca = u"Província",
    es = u"Provincia",
    en = u"Province"
)

translations.define(
    "woost.extensions.locations.location_types.town",
    ca = u"Població",
    es = u"Población",
    en = u"Town"
)

translations.define("Location.code",
    ca = u"Codi",
    es = u"Código",
    en = u"Code"
)

translations.define("Location.parent",
    ca = u"Ubicació pare",
    es = u"Ubicación padre",
    en = u"Parent location"
)

translations.define("Location.locations",
    ca = u"Ubicacions contingudes",
    es = u"Ubicaciones contenidas",
    en = u"Child locations"
)

