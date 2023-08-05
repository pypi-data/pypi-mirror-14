#-*- coding: utf-8 -*-
"""

@author:		Javier Marrero
@contact:		javier.marrero@whads.com
@organization:	Whads/Accent SL
@since:			January 2010
"""
from cocktail.translations import translations

translations.define("woost.extensions.signup.signup_confirmation_controller.title",
    ca = u"Controlador de confirmació d'alta d'usuaris",
    es = u"Controlador de confirmación alta de usuarios",
    en = u"Sign Up confirmation controller"
)

translations.define(
    "woost.extensions.signup.signup_confirmation_email_template.title",
    ca = u"Plantilla de correu electrònic de confirmació d'alta d'usuari",
    es = u"Plantilla de email de confirmación de alta de usuario",
    en = u"Sign Up Confirmation email template"
)

translations.define(
    "woost.extensions.signup.signup_confirmation_email_template.subject",
    ca = u"Confirmació de compte d'usuari",
    es = u"Confirmación de cuenta de usuario",
    en = u"User account confirmation"
)

translations.define(
    "woost.extensions.signup.signup_confirmation_email_template.body",
    ca = u"Hola ${user.email}:<br/><br/>"
         u"Fes clic per confirmar el teu compte d'usuari:<br/>"
         u"<a href='${confirmation_url}'>${confirmation_url}</a>",
    es = u"Hola ${user.email}:<br/><br/>"
         u"Haz clic para confirmar tu cuenta de usuario:<br/>"
         u"<a href='${confirmation_url}'>${confirmation_url}</a>",
    en = u"Hello ${user.email},<br/><br/>"
         u"Click here to confirm your email account:<br/>"
         u"<a href='${confirmation_url}'>${confirmation_url}</a>",
    pt = u"""Olá ${user.email}:<br/><br/>
Clique para confirmar a sua conta de utilizador:<br/>
<a href='${confirmation_url}'>${confirmation_url}</a>"""
)

translations.define(
    "woost.extensions.signup.signup_page.title",
    ca = u"Registre d'usuari",
    es = u"Registro de usuario",
    en = u"Sign Up"
)

translations.define(
    "woost.extensions.signup.signup_pending_page.title",
    ca = u"Alta d'usuari pendent de confirmació",
    es = u"Alta de usuario pendiente de confirmación",
    en = u"Sign Up pending of confirmation"
)

translations.define("woost.extensions.signup.signup_pending_text_block.text",
    ca = u"""
        En breu rebrà un missatge a la bústia de
        correu electrònic que ens ha facilitat. Segueixi les indicacions del
        correu per tal de confirmar la seva alta a la web. Gràcies.
    """,
    es = u"""
        En breve recibirá un mensaje en el buzón de
        correo electrónico que nos ha indicado. Siga los pasos que allí le
        indicamos para que confirme su alta en la web. Gracias.
    """,
    en = u"""
        We've sent you an email with the necessary
        instructions to complete the registration process.
    """,
    pt = u"""
        Em poucos momentos receberá um mail de
        confirmação do registo.
    """
)

translations.define(
    "woost.extensions.signup.signup_confirmation_page.title",
    ca = u"Alta realitzada amb èxit",
    es = u"Alta realizada con éxito",
    en = u"Thanks for signing up!",
    pt = u"Obrigado por se inscrever"
)

translations.define("woost.extensions.signup.signup_confirmation_text_block.text",
    ca = u"El procés d'alta d'usuari s'ha realitzat correctament.",
    es = u"El proceso de alta de usuario se ha completado correctamente.",
    en = u"The user registration process has been completed successfully.",
    pt = u"Registro confirmado."
)

# SignUpBlock
#------------------------------------------------------------------------------
translations.define("SignUpBlock",
    ca = u"Alta d'usuari",
    es = u"Alta de usuario",
    en = u"Sign up"
)

translations.define("SignUpBlock-plural",
    ca = u"Alta d'usuari",
    es = u"Alta de usuario",
    en = u"Sign up"
)

translations.define("SignUpBlock.signup_process",
    ca = u"Procés d'alta",
    es = u"Proceso de alta",
    en = u"Sign up process"
)

translations.define("SignUpBlock.user_type",
    ca = u"Tipus d'usuari",
    es = u"Tipo de usuario",
    en = u"User type"
)

translations.define("SignUpBlock.roles",
    ca = u"Rols per defecte",
    es = u"Roles por defecto",
    en = u"Default roles"
)

translations.define("SignUpBlock.roles-explanation",
    ca = u"Rols que seran assignats després de l'alta",
    es = u"Roles que serán asigandos tras el alta",
    en = u"Roles that will be assigned after sign up"
)

translations.define("SignUpBlock.confirmation_page",
    ca = u"Pàgina de confirmació",
    es = u"Página de confirmación",
    en = u"Confirmation page"
)

translations.define("SignUpBlock.confirmation_page-explanation",
    ca = u"Pàgina on finalitza el procés d'alta i es gestiona la confirmació si correspon",
    es = u"Página donde finaliza el proceso de alta y se gestiona la confirmación si corresponde",
    en = u"Page where ends the sign up process and will be take place the sign up confirmation process if is required"
)

translations.define("SignUpBlock.pending_page",
    ca = u"Pàgina de registre en espera",
    es = u"Página de registro en espera",
    en = u"Sign up pending page"
)

translations.define("SignUpBlock.confirmation_email_template",
    ca = u"Plantilla de correu electrònic de confirmació",
    es = u"Plantilla de correo electrónico de confirmación",
    en = u"Sign up email template"
)

translations.define("SignUpBlock.confirmation_email_template-explanation",
    ca = u"""Assignar una plantilla de correu electrònic de confirmació activa
        automàticament el sistema de confirmació per correu electrònic en el
        procés d'alta.""",
    es = u"""Asignar una plantilla de email de confirmación, activa
        automáticamente el sistema de confirmación por email en el proceso de
        alta""",
    en = u"""Selecting a sign up email template will automatically enable the
        email confirmation system in the sign up process"""
)

translations.define("SignUpForm.password_confirmation",
    ca = u"Confirmar la contrasenya",
    es = u"Confirmar la contraseña",
    en = u"Confirm password",
    pt = u"Confirmar Palavra-passe"
)

# User
#------------------------------------------------------------------------------
translations.define("User.confirmed_email",
    ca = u"Correu electrònic confirmat",
    es = u"Correo electrónico confirmado",
    en = u"Confirmed email"
)
