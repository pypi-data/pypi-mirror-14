#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.stringutils import decapitalize
from cocktail.translations import translations
from cocktail.translations.helpers import plural2, ca_possessive, join
from woost.translations.strings \
    import content_permission_translation_factory

translations.define("woost.type_groups.translation_workflow",
    ca = u"Circuït de traducció",
    es = u"Circuito de traducción",
    en = u"Translation workflow"
)

translations.define("woost.actions.translation_workflow_transition",
    ca = u"Canviar estat",
    es = u"Cambiar estado",
    en = u"Change state"
)

translations.define("woost.extensions.translationworkflow.translation_path",
    ca = lambda source_language, target_language, **kwargs:
        ca_possessive(translations("locale", locale = source_language).lower())
        + u" a "
        + translations("locale", locale = target_language).lower(),
    es = lambda source_language, target_language, **kwargs:
        u"De "
        + translations("locale", locale = source_language).lower()
        + u" a "
        + translations("locale", locale = target_language).lower(),
    en = lambda source_language, target_language, **kwargs:
        u"From "
        + translations("locale", locale = source_language).lower()
        + u" to "
        + translations("locale", locale = target_language).lower()
)

translations.define(
    "woost.extensions.translationworkflow.transitionaction."
    "TranslationWorkflowInvalidTextError-instance",
    ca = lambda instance:
        u"<em>%s</em> conté errors que impedeixen passar-la a l'estat "
        u"<em>%s</em> (%s)" % (
            translations(instance.request),
            translations(instance.transition.target_state).lower(),
            translations(instance.error)
        ),
    es = lambda instance:
        u"<em>%s</em> contiene errores que impiden pasarla al estado "
        u"<em>%s</em> (%s)" % (
            translations(instance.request),
            translations(instance.transition.target_state).lower(),
            translations(instance.error)
        ),
    en = lambda instance:
        u"<em>%s</em> contains errors that prevent its transition to the "
        u"<em>%s</em> state (%s)" % (
            translations(instance.request),
            translations(instance.transition.target_state).lower(),
            translations(instance.error)
        )
)

# Configuration
#------------------------------------------------------------------------------
translations.define("Configuration.translation_workflow_paths",
    ca = u"Camins de traducció",
    es = u"Caminos de traducción",
    en = u"Translation paths"
)

translations.define("Configuration.translation_workflow_paths-explanation",
    ca = u"Emparellaments d'idiomes per generar peticions de traducció.",
    es = u"Emparejamientos de idiomas para generar peticiones de traducción.",
    en = u"Language pairings to generate translation requests."
)

# User
#------------------------------------------------------------------------------
translations.define("User.translation_proficiencies",
    ca = u"Traduccions que pot realitzar",
    es = u"Traducciones que puede realizar",
    en = u"Translations he/she can perform"
)

translations.define("User.managed_translation_agency",
    ca = u"Agència de traducció que gestiona",
    es = u"Agencia de traducción que gestiona",
    en = u"Managed translation agency"
)

translations.define("User.translation_agency",
    ca = u"Agència de traducció per la que treballa",
    es = u"Agencia de traducción para la que trabaja",
    en = u"Translation agency he/she works for"
)

# Item
#------------------------------------------------------------------------------
translations.define("Item.translation_requests",
    ca = u"Peticions de traducció",
    es = u"Peticiones de traducción",
    en = u"Translation requests"
)

# Role
#------------------------------------------------------------------------------
translations.define("Role.translation_workflow_relevant_states",
    ca = u"Estats rellevants del circuït de traducció",
    es = u"Estados relevantes del circuito de traducción",
    en = u"Translation workflow relevant states"
)

translations.define("Role.translation_workflow_default_state",
    ca = u"Estat per defecte del circuït de traducció",
    es = u"Estado por defecto del circuito de traducción",
    en = u"Translation workflow default state"
)

translations.define("Role.translation_workflow_default_transition",
    ca = u"Transició per defecte del circuït de traducció",
    es = u"Transición por defecto del circuito de traducción",
    en = u"Translation workflow default transition"
)

translations.define("Role.translation_workflow_default_transition_condition",
    ca = u"Condició per la transició per defecte del circuït de traducció",
    es = u"Condición para la transición por defecto del circuito de traducción",
    en = u"Condition for the translation workflow default transition"
)

# TranslationWorkflowRequest
#------------------------------------------------------------------------------
translations.define("TranslationWorkflowRequest",
    ca = u"Petició de traducció",
    es = u"Petición de traducción",
    en = u"Translation request"
)

translations.define("TranslationWorkflowRequest-plural",
    ca = u"Peticions de traducció",
    es = u"Peticiones de traducción",
    en = u"Translation requests"
)

translations.define("TranslationWorkflowRequest.tabs.all",
    ca = u"Totes",
    es = u"Todas",
    en = u"All"
)

translations.define("TranslationWorkflowRequest.translation_request",
    ca = u"Petició de traducció",
    es = u"Petición de traducción",
    en = u"Translation request"
)

translations.define("TranslationWorkflowRequest.translation_request.info",
    ca = u"Dades de la petició",
    es = u"Datos de la petición",
    en = u"Request data"
)

translations.define("TranslationWorkflowRequest.translation_request.translated_values",
    ca = u"Traducció",
    es = u"Traducción",
    en = u"Translation"
)

translations.define("TranslationWorkflowRequest.translation_request.changelog",
    ca = u"Històric",
    es = u"Histórico",
    en = u"Change log"
)

translations.define("TranslationWorkflowRequest.translated_item",
    ca = u"Element a traduir",
    es = u"Elemento a traducir",
    en = u"Translated item"
)

translations.define("TranslationWorkflowRequest.source_language",
    ca = u"Idioma origen",
    es = u"Idioma origen",
    en = u"Idioma destino"
)

translations.define("TranslationWorkflowRequest.target_language",
    ca = u"Idioma destí",
    es = u"Idioma destino",
    en = u"Target language"
)

translations.define("TranslationWorkflowRequest.state",
    ca = u"Estat",
    es = u"Estado",
    en = u"State"
)

translations.define("TranslationWorkflowRequest.assigned_agency",
    ca = u"Agència de traducció",
    es = u"Agencia de traducción",
    en = u"Translation agency"
)

translations.define("TranslationWorkflowRequest.assigned_translator",
    ca = u"Traductor assignat",
    es = u"Traductor asignado",
    en = u"Assigned translator"
)

translations.define("TranslationWorkflowRequest.translated_values",
    ca = u"Traducció",
    es = u"Traducción",
    en = u"Translation"
)

translations.define("TranslationWorkflowRequest.comments",
    ca = u"Comentaris",
    es = u"Comentarios",
    en = u"Comments"
)

translations.define(
    "woost.extensions.translationworkflow.request."
    "TranslationWorkflowRequest-instance",
    ca = lambda instance, referer = None, **kwargs:
        (
            (
                u"Traducció "
                + ca_possessive(
                     '"%s" '
                     % translations(instance.translated_item)
                )
            )
            if referer is None
            else ""
        )
        + (
            instance.source_language
            and ca_possessive(
                decapitalize(
                    translations("locale", locale = instance.source_language)
                )
            )
            or u"?"
        )
        + u" a "
        + (
            instance.target_language
            and decapitalize(
                translations("locale", locale = instance.target_language)
            )
            or u"?"
        ),
    es = lambda instance, referer = None, **kwargs:
        (
            u'Traducción de "%s" de '
            % translations(instance.translated_item)
            if referer is None
            else u"De "
        )
        + (
            instance.source_language
            and decapitalize(
                translations("locale", locale = instance.source_language)
            )
            or u"?"
        )
        + u" a "
        + (
            decapitalize(
                translations("locale", locale = instance.target_language)
            )
            if instance.target_language
            else "?"
        ),
    en = lambda instance, referer = None, **kwargs:
        (
            u'Translation of "%s" from '
            % translations(instance.translated_item)
            if referer is None
            else u"From "
        )
        + (
            instance.source_language
            and translations("locale", locale = instance.source_language)
            or u"?"
        )
        + u" to "
        + (
            instance.target_language
            and translations("locale", locale = instance.target_language)
            or u"?"
        )
)

translations.define("TranslationWorkflowRequest.msexcel.source",
    ca = u"Text original",
    es = u"Texto original",
    en = u"Source text"
)

translations.define("TranslationWorkflowRequest.msexcel.target",
    ca = u"Traducció",
    es = u"Traducción",
    en = u"Translation"
)

# TranslationWorkflowState
#------------------------------------------------------------------------------
translations.define("TranslationWorkflowState",
    ca = u"Estat del circuït de traducció",
    es = u"Estado del circuito de traducción",
    en = u"Translation workflow state"
)

translations.define("TranslationWorkflowState-plural",
    ca = u"Estats del circuït de traducció",
    es = u"Estados del circuito de traducción",
    en = u"Translation workflow states"
)

translations.define("TranslationWorkflowState.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("TranslationWorkflowState.plural_title",
    ca = u"Nom en plural",
    es = u"Nombre en plural",
    en = u"Plural name"
)

translations.define("TranslationWorkflowState.color",
    ca = u"Color",
    es = u"Color",
    en = u"Color"
)

translations.define("TranslationWorkflowState.incomming_transitions",
    ca = u"Transicions entrants",
    es = u"Transiciones entrantes",
    en = u"Incomming transitions"
)

translations.define("TranslationWorkflowState.outgoing_transitions",
    ca = u"Transicions de sortida",
    es = u"Transiciones de salida",
    en = u"Outgoing transitions"
)

translations.define("TranslationWorkflowState.state_after_source_change",
    ca = u"Nou estat quan es modifiqui el text original",
    es = u"Nuevo estado cuando se modifique el texto original",
    en = u"State after the translated item is modified"
)

translations.define("TranslationWorkflowState.requests",
    ca = u"Peticions de traducció",
    es = u"Peticiones de traducción",
    en = u"Translation requests"
)

# TranslationWorkflowTransition
#------------------------------------------------------------------------------
translations.define("TranslationWorkflowTransition",
    ca = u"Transició del circuït de traducció",
    es = u"Transición del circuito de traducción",
    en = u"Translation workflow transition"
)

translations.define("TranslationWorkflowTransition-plural",
    ca = u"Transicions del circuït de traducció",
    es = u"Transiciones del circuito de traducción",
    en = u"Translation workflow transitions"
)

translations.define("TranslationWorkflowTransition.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("TranslationWorkflowTransition.source_states",
    ca = u"Estat origen",
    es = u"Estado origen",
    en = u"Source state"
)

translations.define("TranslationWorkflowTransition.source_states-explanation",
    ca = u"Els estats on comença la transició. Deixar en blanc per definir "
         u"una transició aplicable a tots els estats.",
    es = u"Los estados desde los que parte la transición. Dejar en blanco "
         u"para definir una transición aplicable a todos los estados.",
    en = u"The starting states for the transition. Leave blank to define a "
         u"transition that can be applied to any state."
)

translations.define("TranslationWorkflowTransition.target_state",
    ca = u"Estat destí",
    es = u"Estado destino",
    en = u"Target state"
)

translations.define("TranslationWorkflowTransition.icon",
    ca = u"Icona",
    es = u"Icono",
    en = u"Icon"
)

translations.define("TranslationWorkflowTransition.relative_order",
    ca = u"Ordre relatiu",
    es = u"Orden relativo",
    en = u"Relative order"
)

translations.define("TranslationWorkflowTransition.requires_valid_text",
    ca = u"Requereix validació del text",
    es = u"Requiere validación del texto",
    en = u"Requires text validation"
)

translations.define("TranslationWorkflowTransition.requires_different_state",
    ca = u"Deshabilitar per peticions a l'estat destí",
    es = u"Deshabilitar para peticiones en el estado destino",
    en = u"Disable for requests in the target state"
)

translations.define("TranslationWorkflowTransition.transition_setup_class",
    ca = u"Codi de preparació de la transició",
    es = u"Código de preparación de la transición",
    en = u"Transition setup code"
)

translations.define("TranslationWorkflowTransition.transition_code",
    ca = u"Codi de transició",
    es = u"Código de transición",
    en = u"Transition code"
)

translations.define(
    "woost.extensions.translationworkflow.transitions_notice",
    ca = lambda new_state, count:
        plural2(
            count,
            u"Una petició passada",
            u"%d peticions passades" % count
        )
        + u" a l'estat <em>%s</em>."
          % decapitalize(translations(new_state)),
    es = lambda new_state, count:
        plural2(
            count,
            u"Una petición pasada",
            u"%d peticiones pasadas" % count
        )
        + u" al estado <em>%s</em>."
          % decapitalize(translations(new_state)),
    en = lambda new_state, count:
        plural2(
            count,
            u"One request",
            u"%d requests" % count
        )
        + u" transitioned to the <em>%s</em> state."
          % decapitalize(translations(new_state))
)

translations.define(
    "woost.extensions.translationworkflow.silence_notice",
    ca = lambda count:
        plural2(
            len(requests),
            u"S'ha ignorat un canvi a una petició silenciada",
            u"S'han ignorat %d canvis a peticions silenciades" % count
        ),
    es = lambda count:
        plural2(
            count,
            u"Se ha ignorado un cambio a una petición silenciada",
            u"Se han ignorado %d cambios a peticiones silenciadas" % count
        ),
    en = lambda count:
        plural2(
            count,
            u"A change to a silenced request has been ignored",
            u"%d changes to silenced requests have been ignored" % count
        )
)

# TranslationAgency
#------------------------------------------------------------------------------
translations.define("TranslationAgency",
    ca = u"Agència de traducció",
    es = u"Agencia de traducción",
    en = u"Translation agency"
)

translations.define("TranslationAgency-plural",
    ca = u"Agències de traducció",
    es = u"Agencias de traducción",
    en = u"Translation agencies"
)

translations.define("TranslationAgency.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("TranslationAgency.managers",
    ca = u"Gestors",
    es = u"Gestores",
    en = u"Managers"
)

translations.define("TranslationAgency.translators",
    ca = u"Traductors",
    es = u"Traductores",
    en = u"Translators"
)

translations.define("TranslationAgency.translation_proficiencies",
    ca = u"Traduccions que pot realitzar",
    es = u"Traducciones que puede realizar",
    en = u"Translations it can perform"
)

# Transition controller
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.transitionnode."
    "TranslationWorkflowTransitionNode-instance",
    ca = lambda instance:
        instance.transition.title + u" peticions de traducció",
    es = lambda instance:
        instance.transition.title + u" peticiones de traducción",
    en = lambda instance:
        instance.transition.title + u" translation requests"
)

translations.define(
    "woost.extensions.translationworkflow."
    "TranslationWorkflowTransitionView.transition_explanation",
    ca = u"Es canviarà l'estat de les següents peticions:",
    es = u"Se cambiará el estado de las peticiones siguientes:",
    en = u"The state of the following requests will be changed:"
)

translations.define(
    "woost.extensions.translationworkflow."
    "TranslationWorkflowAssignTransitionSetup.assignments",
    ca = u"Assignació de traductors per idiomes",
    es = u"Asignación de traductores por idiomas",
    en = u"Per language translator assignments"
)

# TranslationWorkflowTransitionPermission
#------------------------------------------------------------------------------
translations.define("TranslationWorkflowTransitionPermission",
    ca = u"Permís de transició del circuït de traduccions",
    es = u"Permiso de transición del circuito de traducciones",
    en = u"Translation workflow transition permission"
)

translations.define("TranslationWorkflowTransitionPermission-plural",
    ca = u"Permisos de transició del circuït de traduccions",
    es = u"Permisos de transición del circuito de traducciones",
    en = u"Translation workflow transition permissions"
)

translations.define(
    "woost.extensions.translationworkflow.transitionpermission."
    "TranslationWorkflowTransitionPermission-instance",
    ca = content_permission_translation_factory(
        "ca",
        lambda permission, subject, **kwargs:
            u"aplicar " + (
                join(
                    translations(transition)
                    for transition in permission.transitions
                )
                if permission.transitions else u"canvis d'estat"
            )
            + u" sobre peticions de traducció per " + subject
    ),
    es = content_permission_translation_factory(
        "es",
        lambda permission, subject, **kwargs:
            u"aplicar " + (
                join(
                    translations(transition)
                    for transition in permission.transitions
                )
                if permission.transitions else u"cambios de estado"
            )
            + u" sobre peticiones de traducción para " + subject
    ),
    en = content_permission_translation_factory(
        "en",
        lambda permission, subject, **kwargs:
            u"apply " + (
                join(
                    translations(transition)
                    for transition in permission.transitions
                )
                if permission.transitions else u"state changes"
            )
            + u" to translation requests for " + subject
    )
)

translations.define("TranslationWorkflowTransitionPermission.transitions",
    ca = u"Transicions",
    es = u"Transiciones",
    en = u"Transitions"
)

# TranslationWorkflowComment
#------------------------------------------------------------------------------
translations.define("TranslationWorkflowComment",
    ca = u"Comentari de petició de traducció",
    es = u"Comentario de petición de traducción",
    en = u"Translation request comment"
)

translations.define("TranslationWorkflowComment-plural",
    ca = u"Comentaris de petició de traducció",
    es = u"Comentarios de petición de traducción",
    en = u"Translation request comments"
)

translations.define("TranslationWorkflowComment.request",
    ca = u"Petició",
    es = u"Petición",
    en = u"Request"
)

translations.define("TranslationWorkflowComment.text",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

# TranslationWorkflowTable
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.TranslationWorkflowTable."
    "missing_translation_notice",
    ca = u"Pendent de traduïr",
    es = u"Pendiente de traducción",
    en = u"Not translated yet"
)

# TranslationWorkflowRequestCard
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.TranslationWorkflowRequestCard."
    "request_language_field.field_label",
    ca = u"Idioma",
    es = u"Idioma",
    en = u"Language"
)

# TranslationWorkflowPathEditor
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.TranslationWorkflowPathEditor."
    "source_language_label",
    ca = u"De",
    es = u"De",
    en = u"From"
)

translations.define(
    "woost.extensions.translationworkflow.TranslationWorkflowPathEditor."
    "target_language_label",
    ca = u"a",
    es = u"a",
    en = u"to"
)

# BackOfficeEditViewOverlay
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.translationworkflow.BackOfficeEditViewOverlay."
    "translation_workflow_auto_transition_label",
    ca = lambda transition: u"%s automàticament" % translations(transition),
    es = lambda transition: u"%s automaticamente" % translations(transition),
    en = lambda transition: u"%s automatically" % translations(transition)
)

