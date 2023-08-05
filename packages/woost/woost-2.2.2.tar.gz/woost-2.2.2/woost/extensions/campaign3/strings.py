#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations


# Configuration
#------------------------------------------------------------------------------
translations.define("Configuration.services.campaign_monitor",
    ca = u"Campaign Monitor",
    es = u"Campaign Monitor",
    en = u"Campaign Monitor"
)

translations.define("Configuration.campaign_monitor_api_key",
    ca = u"Clau d'API",
    es = u"Clave de API",
    en = u"API key"
)

translations.define("Configuration.campaign_monitor_client_id",
    ca = u"ID de client",
    es = u"ID de cliente",
    en = u"Client ID"
)

# Website
#------------------------------------------------------------------------------
translations.define("Website.services.campaign_monitor",
    ca = u"Campaign Monitor",
    es = u"Campaign Monitor",
    en = u"Campaign Monitor"
)

translations.define("Website.campaign_monitor_api_key",
    ca = u"Clau d'API",
    es = u"Clave de API",
    en = u"API key"
)

translations.define("Website.campaign_monitor_client_id",
    ca = u"ID de client",
    es = u"ID de cliente",
    en = u"Client ID"
)

# CampaignMonitorList
#------------------------------------------------------------------------------
translations.define("CampaignMonitorList",
    ca = u"Llista de subscripció",
    es = u"Lista de suscripción",
    en = u"Subscription list"
)

translations.define("CampaignMonitorList-plural",
    ca = u"Llistes de subscripció",
    es = u"Listas de suscripción",
    en = u"Subscription lists"
)

translations.define("CampaignMonitorList.list_id",
    ca = u"Id de llista",
    es = u"Id de lista",
    en = u"List id"
)

translations.define("CampaignMonitorList.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("CampaignMonitorList.confirmation_page",
    ca = u"Pàgina de confirmació inicial",
    es = u"Página de confirmación inicial",
    en = u"Initial confirmation page"
)

translations.define("CampaignMonitorList.confirmation_page-explanation",
    ca = u"""
Pàgina que es mostrarà després de completar el formulari de subscripció. Si no
s'especifica una pàgina, es mostrarà una pàgina genèrica amb instruccions.
""",
    es = u"""
Página que se mostrará después de completar el formulario de suscripción. Si no
se especifica una página, se mostrará una página genérica con instrucciones.
""",
    en = u"""
The page that will be displayed after someone completes the subscribe form. If
you don't specify a page, a generic page with instructions will be displayed to
the subscriber.
"""
)

translations.define("CampaignMonitorList.confirmation_success_page",
    ca = u"Pàgina de confirmació d'alta",
    es = u"Página de confirmación de alta",
    en = u"Confirmation success page"
)

translations.define("CampaignMonitorList.confirmation_success_page-explanation",
    ca = u"""
Pàgina que es mostrarà després que un subscriptor faci clic a l'enllaç de
confirmació en el correu de verificació. Si no s'especifica una pàgina, es
mostrarà una pàgina de gràcies genèrica.
""",
    es = u"""
Página que se mostrará después de que un suscriptor haga clic en el enlace de
confirmación en el correo de verificación. Si no se especifica una página, se
mostrará una página de gracias genérica.
""",
    en = u"""
Page that will be displayed after the subscriber clicks the confirmation link
in the verification email. If you don't specify a page, a generic thank you
page will be displayed to the subscriber.
"""
)

translations.define("CampaignMonitorList.unsubscribe_page",
    ca = u"Pàgina de baixa",
    es = u"Página de baja",
    en = u"Unsubscribe page"
)

translations.define("CampaignMonitorList.unsubscribe_page-explanation",
    ca = u"""
Pàgina que es mostrarà després que un subscriptor faci clic a l'enllaç de baixa
en un correu. Si no s'especifica una pàgina, es mostrarà una pàgina de
confirmació generica.
""",
    es = u"""
Página que se mostrará después de que un suscriptor haga clic en el enlace de
baja en un correo. Si no se especifica una página, se mostrará una pàgina de
confirmación generica.
""",
    en = u"""
Page that will be displayed after someone clicks an unsubscribe link in your
email. If you don't specify a page, a generic confirmation page will be
displayed to the subscriber.
"""
)

# CampaignMonitorListEditNode
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode synchronized changes",
    ca = lambda item:
        u"Canvis a <strong>%s</strong> sincronitzats" % (
            translations(item, "ca"),
        ),
    es = lambda item:
        u"Cambios en <strong>%s</strong> sincronizados" % (
            translations(item, "es"),
        ),
    en = lambda item:
        u"Synchronized changes to <strong>%s</strong>" % (
            translations(item, "en"),
        )
)

translations.define(
    "woost.extensions.campaignmonitorlisteditnode.CampaignMonitorListEditNode failed synchronization",
    ca = lambda item, exception:
        u"Sincronització de <strong>%s</strong> fallida. <em>%s</em>" % (
            translations(item, "ca"),
            unicode(exception)
        ),
    es = lambda item, exception:
        u"Sincronización de <strong>%s</strong> fallida. <em>%s</em>" % (
            translations(item, "es"),
            unicode(exception)
        ),
    en = lambda item, exception:
        u"<strong>%s</strong> synchronization failed. <em>%s</em>" % (
            translations(item, "en"),
            unicode(exception)
        )
)

# Subscriber
#------------------------------------------------------------------------------
translations.define("Subscriber.subscriber_name",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Subscriber.subscriber_email",
    ca = u"Correu electrònic",
    es = u"Correo electrónico",
    en = u"Email"
)

translations.define("subscription_form.lists",
    ca = u"Llistes",
    es = u"Listas",
    en = u"Lists"
)

# SubscriptionFormBlock
#------------------------------------------------------------------------------
translations.define("SubscriptionFormBlock",
    ca = u"Formulari de subscripció",
    es = u"Formulario de suscripción",
    en = u"Subscription form"
)

translations.define("SubscriptionFormBlock-plural",
    ca = u"Formulari de subscripció",
    es = u"Formulario de suscripción",
    en = u"Subscription form"
)

translations.define("SubscriptionFormBlock.subscriber_model",
    ca = u"Model de subscriptor",
    es = u"Modelo de suscriptor",
    en = u"Subscription model"
)

translations.define("SubscriptionFormBlock.lists",
    ca = u"Llistes",
    es = u"Listas",
    en = u"Lists"
)

translations.define("SubscriptionFormBlock.view_class",
    ca = u"Vista",
    es = u"Vista",
    en = u"View"
)

# ResubscribeFormView
#------------------------------------------------------------------------------
translations.define("woost.extensions.campaign3.ResubscribeFormView.unsubscribed_by_error",
    ca = u"<strong>No volies donar-te de baixa?</strong> Clica a continuació per seguir rebent els nostres missatges.",
    es = u"<strong>No querías darte de baja?</strong> Haz clic a continuación para seguir recibiendo nuestros mensajes.",
    en = u"<strong>You did not want to unsubscribe?</strong> Click below to continue receiving our messages."
)

translations.define("woost.extensions.campaign3.ResubscribeFormView.resubscribe",
    ca = u"Tornar a subscriure's",
    es = u"Volver a suscribirse",
    en = u"Re-subscribe"
)

