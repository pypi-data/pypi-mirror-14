#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.iteration import first
from cocktail.translations import translations, get_language
from woost.extensions.locations.location import Location

# Override the translation for locales to replace country ISO codes with
# human readable descriptions

def _translate_locale(locale):

    parts = locale.split("-")
    parts[0] = translations(parts[0], default = parts[0])

    if len(parts) > 1:
        location = first(
            Location.select({
                "location_type": "country",
                "code": parts[1]
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

            if location_name:
                parts[1] = location_name

    return " - ".join(parts)

translations.define("locale", **dict(
    (lang, _translate_locale)
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

