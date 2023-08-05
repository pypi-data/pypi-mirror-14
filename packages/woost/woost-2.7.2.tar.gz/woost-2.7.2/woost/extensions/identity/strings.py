#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from cocktail.translations import translations

# Configuration
#------------------------------------------------------------------------------
translations.define("Configuration.identity_providers",
    ca = u"Serveis d'autenticació d'usuaris",
    es = u"Servicios de autenticación de usuarios",
    en = u"User authentication services"
)

# User
#------------------------------------------------------------------------------
translations.define("User.google_user_id",
    ca = u"Id de Google",
    es = u"Id de Google",
    en = u"Google ID"
)

translations.define("User.facebook_user_id",
    ca = u"Id de Facebook",
    es = u"Id de Facebook",
    en = u"Facebook ID"
)

# IdentityProvider
#------------------------------------------------------------------------------
translations.define("IdentityProvider",
    ca = u"Servei d'autenticació d'usuaris",
    es = u"Servicio de autenticación de usuarios",
    en = u"User authentication service"
)

translations.define("IdentityProvider-plural",
    ca = u"Serveis d'autenticació d'usuaris",
    es = u"Servicios de autenticación de usuarios",
    en = u"User authentication services"
)

translations.define("IdentityProvider.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("IdentityProvider.hidden",
    ca = u"Ocult",
    es = u"Oculto",
    en = u"Hidden"
)

translations.define("IdentityProvider.debug_mode",
    ca = u"Mostrar informació per desenvolupadors",
    es = u"Mostrar información para desarrolladores",
    en = "Enable debugging"
)

# FacebookIdentityProvider
#------------------------------------------------------------------------------
translations.define("FacebookIdentityProvider",
    ca = u"Servei d'autenticació de Facebook",
    es = u"Servicio de autenticación de Facebook",
    en = u"Facebook authentication service"
)

translations.define("FacebookIdentityProvider-plural",
    ca = u"Serveis d'autenticació de Facebook",
    es = u"Servicios de autenticación de Facebook",
    en = u"Facebook authentication services"
)

translations.define("FacebookIdentityProvider.client_id",
    ca = u"Identificador de client",
    es = u"Identificador de cliente",
    en = u"Client id"
)

translations.define("FacebookIdentityProvider.client_id-explanation",
    ca = u"Un identificador únic de l'aplicació de Facebook que s'utilitzarà "
         u"per gestionar l'autenticació. S'obté des del panell de "
         u"configuració de l'aplicació de Facebook.",
    es = u"Un identificador único de la aplicación de Facebook que se "
         u"utilizará para gestionar la autenticación. Se obtiene desde el "
         u"panel de configuración de la aplicación de Facebook.",
    en = u"The unique identifier of the application that is to be used to "
         u"mediate the authentication process. Obtained from the Facebook "
         u"application configuration panel."
)

translations.define("FacebookIdentityProvider.client_secret",
    ca = u"Secret de client",
    es = u"Secreto de cliente",
    en = u"Client secret"
)

translations.define("FacebookIdentityProvider.client_secret-explanation",
    ca = u"La contrasenya de l'aplicació de Facebook que s'utilitzarà "
         u"per gestionar l'autenticació. S'obté des del panell de "
         u"configuració de l'aplicació de Facebook.",
    es = u"La contraseña de la aplicación de Facebook que se "
         u"utilizará para gestionar la autenticación. Se obtiene desde el "
         u"panel de configuración de la aplicación de Facebook.",
    en = u"The password for the application that is to be used to "
         u"mediate the authentication process. Obtained from the Facebook "
         u"application configuration panel."
)

translations.define("FacebookIdentityProvider.scope",
    ca = u"Privilegis a sol·licitar",
    es = u"Privilegios a solicitar",
    en = u"Requested scope"
)

# GoogleIdentityProvider
#------------------------------------------------------------------------------
translations.define("GoogleIdentityProvider",
    ca = u"Servei d'autenticació de Google",
    es = u"Servicio de autenticación de Google",
    en = u"Google authentication service"
)

translations.define("GoogleIdentityProvider-plural",
    ca = u"Serveis d'autenticació de Google",
    es = u"Servicios de autenticación de Google",
    en = u"Google authentication services"
)

translations.define("GoogleIdentityProvider.client_id",
    ca = u"Identificador de client",
    es = u"Identificador de cliente",
    en = u"Client id"
)

translations.define("GoogleIdentityProvider.client_id-explanation",
    ca = u"Un identificador únic de l'aplicació de Google que s'utilitzarà "
         u"per gestionar l'autenticació. S'obté a la consola de "
         u"desenvolupament de Google.",
    es = u"Un identificador único de la aplicación de Google que se "
         u"utilizará para gestionar la autenticación. Se obtiene desde la "
         u"consola de desarrollo de Google.",
    en = u"The unique identifier of the application that is to be used to "
         u"mediate the authentication process. Obtained from the Google "
         u"development console."
)

translations.define("GoogleIdentityProvider.client_secret",
    ca = u"Secret de client",
    es = u"Secreto de cliente",
    en = u"Client secret"
)

translations.define("GoogleIdentityProvider.client_secret-explanation",
    ca = u"La contrasenya de l'aplicació de Google que s'utilitzarà "
         u"per gestionar l'autenticació. S'obté a la consola de "
         u"desenvolupament de Google.",
    es = u"La contraseña de la aplicación de Google que se "
         u"utilizará para gestionar la autenticación. Se obtiene desde la "
         u"consola de desarrollo de Google.",
    en = u"The password for the application that is to be used to "
         u"mediate the authentication process. Obtained from the Google "
         u"development console."
)

translations.define("GoogleIdentityProvider.scope",
    ca = u"Privilegis a sol·licitar",
    es = u"Privilegios a solicitar",
    en = u"Requested scope"
)

translations.define("GoogleIdentityProvider.access_type",
    ca = u"Tipus d'accés",
    es = u"Tipo de acceso",
    en = u"Access type"
)

translations.define("GoogleIdentityProvider.access_type=online",
    ca = u"En línia",
    es = u"En línea",
    en = u"Online"
)

translations.define("GoogleIdentityProvider.access_type=offline",
    ca = u"Fora de línia",
    es = u"Fuera de línea",
    en = u"Offline"
)

