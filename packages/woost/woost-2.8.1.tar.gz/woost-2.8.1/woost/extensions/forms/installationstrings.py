#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

translations.define(
    "woost.extensions.forms.default_email_notification.title",
    ca = u"Notificació per formularis personalitzats",
    es = u"Notificación para formularios personalizados",
    en = u"Notification for custom forms",
)

translations.define(
    "woost.extensions.forms.default_email_notification.subject",
    ca = u"S'ha emplenat ${form_description}",
    es = u"Se ha rellenado ${form_description}",
    en = u"${form_description} submitted"
)

translations.define(
    "woost.extensions.forms.default_email_notification.body",
    ca = u"""${form_contents}""",
    es = u"""${form_contents}""",
    en = u"""${form_contents}"""
)

