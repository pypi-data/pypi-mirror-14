#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.translations.helpers import plural2

translations.define("woost.actions.survey_results",
    ca = u"Veure resultats",
    es = u"Ver resultados",
    en = u"View results"
)

# Survey
#------------------------------------------------------------------------------
translations.define("Survey",
    ca = u"Enquesta",
    es = u"Encuesta",
    en = u"Survey"
)

translations.define("Survey-plural",
    ca = u"Enquesta",
    es = u"Encuesta",
    en = u"Survey"
)

translations.define("Survey.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("Survey.questions",
    ca = u"Preguntes",
    es = u"Preguntas",
    en = u"Questions"
)

# SurveyQuestion
#------------------------------------------------------------------------------
translations.define("SurveyQuestion",
    ca = u"Pregunta d'enquesta",
    es = u"Pregunta de encuesta",
    en = u"Survey question"
)

translations.define("SurveyQuestion-plural",
    ca = u"Preguntes d'enquestes",
    es = u"Preguntas de encuesta",
    en = u"Survey questions"
)

translations.define("SurveyQuestion.title",
    ca = u"Enunciat",
    es = u"Enunciado",
    en = u"Question"
)

translations.define("SurveyQuestion.survey",
    ca = u"Enquesta",
    es = u"Encuesta",
    en = u"Survey"
)

translations.define("SurveyQuestion.active",
    ca = u"Activa",
    es = u"Activa",
    en = u"Active"
)

# SurveyOptionsQuestion
#------------------------------------------------------------------------------
translations.define("SurveyOptionsQuestion",
    ca = u"Pregunta amb opcions",
    es = u"Pregunta con opciones",
    en = u"Options question"
)

translations.define("SurveyOptionsQuestion-plural",
    ca = u"Preguntes amb opcions",
    es = u"Preguntas con opciones",
    en = u"Options questions"
)

translations.define("SurveyOptionsQuestion.options",
    ca = u"Opcions",
    es = u"Opciones",
    en = u"Options"
)

# SurveyOption
#------------------------------------------------------------------------------
translations.define("SurveyOption",
    ca = u"Opció",
    es = u"Opción",
    en = u"Option"
)

translations.define("SurveyOption-plural",
    ca = u"Opcions",
    es = u"Opciones",
    en = u"Options"
)

translations.define("SurveyOption.title",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define("SurveyOption.active",
    ca = u"Activa",
    es = u"Activa",
    en = u"Active"
)

# SurveyTextQuestion
#------------------------------------------------------------------------------
translations.define("SurveyTextQuestion",
    ca = u"Pregunta de text lliure",
    es = u"Pregunta de texto libre",
    en = u"Text question"
)

translations.define("SurveyTextQuestion-plural",
    ca = u"Preguntes de text lliure",
    es = u"Preguntas de texto libre",
    en = u"Text questions"
)

translations.define("SurveyTextQuestion.mandatory",
    ca = u"Obligatòria",
    es = u"Obligatoria",
    en = u"Mandatory"
)

# SurveyBlock
#------------------------------------------------------------------------------
translations.define("SurveyBlock",
    ca = u"Formulari d'enquesta",
    es = u"Formulario de encuesta",
    en = u"Survey form"
)

translations.define("SurveyBlock-plural",
    ca = u"Formularis d'enquesta",
    es = u"Formularios de encuesta",
    en = u"Survey forms"
)

translations.define("SurveyBlock.survey",
    ca = u"Enquesta",
    es = u"Encuesta",
    en = u"Survey"
)

translations.define("SurveyBlock.redirection",
    ca = u"Redirecció",
    es = u"Redirección",
    en = u"Redirection"
)

translations.define("SurveyBlock.redirection-explanation",
    ca = u"La pàgina on es rediregeix als usuaris que completin l'enquesta.",
    es = u"La página donde se redirige a los usuarios que completen la "
         "encuesta.",
    en = u"The page where users who complete the survey will be redirected."
)

# SurveyResultsView
#------------------------------------------------------------------------------
translations.define(
    "woost.extensions.surveys.SurveyResultsView.answers_heading",
    ca = u"Respostes",
    es = u"Respuestas",
    en = u"Answers"
)

translations.define(
    "woost.extensions.surveys.SurveyResultsView.submission_count",
    ca = lambda count:
        u"L'enquesta " + (
            u"encara no ha estat emplenada per cap usuari"
            if not count
            else (
                u"ha estat emplenada per <strong>%d</strong> " % count
                + plural2(count, u"usuari", u"usuaris")
            )
            + "."
        ),
    es = lambda count:
        u"La encuesta " + (
            u"todavía no sido contestada por ningún usuario"
            if not count
            else (
                u"ha sido contestada por <strong>%d</strong> " % count
                + plural2(count, u"usuario", u"usuarios")
            )
            + "."
        ),
    en = lambda count:
        u"The survey " + (
            u"hasn't been answered by anybody yet"
            if not count
            else (
                u"has been answered by <strong>%d</strong> " % count
                + plural2(count, u"user", u"users")
            )
            + "."
        )
)

translations.define(
    "woost.extensions.surveys.SurveyResultsView.download_excel_link",
    ca = u"Descarregar totes les respostes",
    es = u"Descargar todas las respuestas",
    en = u"Download all answers"
)

