#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

# States
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.states.pending.title",
    ca = u"Pendent d'avaluar",
    es = u"Pendiente de evaluar",
    en = u"Evaluation pending"
)

translations.define(
    "woost.extensions.translationworkflow.states.pending.plural_title",
    ca = u"Pendents d'avaluar",
    es = u"Pendientes de evaluar",
    en = u"Evaluation pending"
)

translations.define(
    "woost.extensions.translationworkflow.states.ignored.title",
    ca = u"Ignorada",
    es = u"Ignorada",
    en = u"Ignored"
)

translations.define(
    "woost.extensions.translationworkflow.states.ignored.plural_title",
    ca = u"Ignorades",
    es = u"Ignoradas",
    en = u"Ignored"
)

translations.define(
    "woost.extensions.translationworkflow.states.silenced.title",
    ca = u"Silenciada",
    es = u"Silenciada",
    en = u"Silenced"
)

translations.define(
    "woost.extensions.translationworkflow.states.silenced.plural_title",
    ca = u"Silenciades",
    es = u"Silenciadas",
    en = u"Silenced"
)

translations.define(
    "woost.extensions.translationworkflow.states.selected.title",
    ca = u"Seleccionada",
    es = u"Seleccionada",
    en = u"Selected"
)

translations.define(
    "woost.extensions.translationworkflow.states.selected.plural_title",
    ca = u"Seleccionades",
    es = u"Seleccionadas",
    en = u"Selected"
)

translations.define(
    "woost.extensions.translationworkflow.states.sent_to_agency.title",
    ca = u"Enviada a agència",
    es = u"Enviada a agencia",
    en = u"Sent to agency"
)

translations.define(
    "woost.extensions.translationworkflow.states.sent_to_agency.plural_title",
    ca = u"Enviades a agència",
    es = u"Enviadas a agencia",
    en = u"Sent to agency"
)

translations.define(
    "woost.extensions.translationworkflow.states.in_translation.title",
    ca = u"En curs",
    es = u"En curso",
    en = u"In translation"
)

translations.define(
    "woost.extensions.translationworkflow.states.in_translation.plural_title",
    ca = u"En curs",
    es = u"En curso",
    en = u"In translation"
)

translations.define(
    "woost.extensions.translationworkflow.states.proposed.title",
    ca = u"Proposada",
    es = u"Propuesta",
    en = u"Proposed"
)

translations.define(
    "woost.extensions.translationworkflow.states.proposed.plural_title",
    ca = u"Proposades",
    es = u"Propuestas",
    en = u"Proposed"
)

translations.define(
    "woost.extensions.translationworkflow.states.applied.title",
    ca = u"Aplicada",
    es = u"Aplicada",
    en = u"Applied"
)

translations.define(
    "woost.extensions.translationworkflow.states.applied.plural_title",
    ca = u"Aplicades",
    es = u"Aplicadas",
    en = u"Applied"
)

# Transitions
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.transitions.ignore.title",
    ca = u"Ignorar",
    es = u"Ignorar",
    en = u"Ignore"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.silence.title",
    ca = u"Silenciar",
    es = u"Silenciar",
    en = u"Silence"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.select.title",
    ca = u"Seleccionar",
    es = u"Seleccionar",
    en = u"Select"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.reject_selection.title",
    ca = u"Rebutjar",
    es = u"Rechazar",
    en = u"Reject"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.assign.title",
    ca = u"Assignar",
    es = u"Asignar",
    en = u"Assign"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.propose.title",
    ca = u"Proposar traducció",
    es = u"Proponer traducción",
    en = u"Propose translation"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.cancel_proposal.title",
    ca = u"Anul·lar proposta",
    es = u"Anular propuesta",
    en = u"Cancel proposal"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.reject.title",
    ca = u"Rebutjar",
    es = u"Rechazar",
    en = u"Reject"
)

translations.define(
    "woost.extensions.translationworkflow.transitions.accept.title",
    ca = u"Acceptar",
    es = u"Aceptar",
    en = u"Accept"
)

# Transition icons
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.icons.ignore.title",
    ca = u"Icona per la transició 'Ignorar' del circuït de traduccions",
    es = u"Icono para la transición 'Ignorar' del circuito de traducciones",
    en = u"Icon for the 'Ignore' transition of the translation workflow"
)

translations.define(
    "woost.extensions.translationworkflow.icons.silence.title",
    ca = u"Icona per la transició 'Silenciar' del circuït de traduccions",
    es = u"Icono para la transición 'Silenciar' del circuito de traducciones",
    en = u"Icon for the 'Silence' transition of the translation workflow"
)

translations.define(
    "woost.extensions.translationworkflow.icons.forward.title",
    ca = u"Icona per les transicions positives del circuït de traduccions",
    es = u"Icono para las transiciones positivas del circuito de traducciones",
    en = u"Icon for the positive transitions of the translation workflow"
)

translations.define(
    "woost.extensions.translationworkflow.icons.backward.title",
    ca = u"Icona per les transicions negatives del circuït de traduccions",
    es = u"Icono para las transiciones negativas del circuito de traducciones",
    en = u"Icon for the negative transitions of the translation workflow"
)

# Roles
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.roles.coordinators.title",
    ca = u"Coordinadors de traducció",
    es = u"Coordinadores de traducción",
    en = u"Translation coordinators"
)

translations.define(
    "woost.extensions.translationworkflow.roles.translators.title",
    ca = u"Traductors",
    es = u"Traductores",
    en = u"Translators"
)

# Permissions
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow."
    "permissions.translators.modify_assigned_requests.subject_description",
    ca = u"peticions assignades al traductor en estat de traducció",
    es = u"peticiones asignadas al traductor en estado de traducción",
    en = u"requests assigned to the translator and in translation"
)

translations.define(
    "woost.extensions.translationworkflow."
    "permissions.translators.read_requests.subject_description",
    ca = u"peticions assignades al traductor",
    es = u"peticiones asignadas al traductor",
    en = u"requests assigned to the translator"
)

translations.define(
    "woost.extensions.translationworkflow."
    "permissions.translators.read_comments.subject_description",
    ca = u"comentaris de peticions assignades al traductor",
    es = u"comentarios de peticiones asignadas al traductor",
    en = u"comments for requests assigned to the translator"
)

translations.define(
    "woost.extensions.translationworkflow."
    "permissions.translators.write_comments.subject_description",
    ca = u"comentaris de peticions assignades al traductor",
    es = u"comentarios de peticiones asignadas al traductor",
    en = u"comments for requests assigned to the translator"
)

