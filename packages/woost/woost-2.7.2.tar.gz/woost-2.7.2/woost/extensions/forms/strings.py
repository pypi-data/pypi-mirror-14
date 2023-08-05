#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

translations.define("woost.type_groups.custom_forms",
    ca = u"Formularis personalitzats",
    es = u"Formularios personalizados",
    en = u"Custom forms"
)

translations.define("woost.actions.export_form_data",
    ca = u"Exportar les respostes",
    es = u"Exportar las respuestas",
    en = u"Download the answers"
)

translations.define("woost.extensions.forms.submit_date",
    ca = u"Data",
    es = u"Fecha",
    en = u"Date"
)

translations.define("woost.extensions.forms.field_default",
    ca = u"Valor per defecte",
    es = u"Valor por defecto",
    en = u"Default value"
)

translations.define("woost.extensions.forms.field_enumeration",
    ca = u"Valors permesos",
    es = u"Valores permitidos",
    en = u"Allowed values"
)

# FormBlock
#------------------------------------------------------------------------------
translations.define("FormBlock",
    ca = u"Formulari personalitzat",
    es = u"Formulario personalizado",
    en = u"Custom form"
)

translations.define("FormBlock-plural",
    ca = u"Formularis personalitzat",
    es = u"Formularios personalizados",
    en = u"Custom forms"
)

translations.define("FormBlock.form",
    ca = u"Formulari",
    es = u"Formulario",
    en = u"Form"
)

translations.define("FormBlock.field_set",
    ca = u"Conjunt de camps",
    es = u"Conjunto de campos",
    en = u"Field set"
)

translations.define("FormBlock.agreements",
    ca = u"Termes i condicions",
    es = u"Términos y condiciones",
    en = u"Agreements"
)

translations.define("FormBlock.notification_receivers",
    ca = u"Receptors de la notificació",
    es = u"Receptores de la notificación",
    en = u"E-mail notification receivers"
)

translations.define("FormBlock.notification_receivers-explanation",
    ca = u"Indica les adreces de correu electrònic a les que es notificarà "
         u"quan un usuari completi el formulari. Només s'aplica a la "
         u"notificació estàndard: altres notificacions poden tenir altres "
         u"maneres de decidir els seus destinataris.",
    es = u"Indica las direcciones de correo electrónico a las que se "
         u"notificará cuando un usuario complete el formulario. Solo se "
         u"aplica a las notificaciones estándar: otras notificaciones pueden "
         u"tener otras maneras de decidir sus destinatarios.",
    en = u"Indicates the e-mail addresses that should be notified when a user "
         u"submits the form. This only applies to the standard notification: "
         u"other notifications can have different means of deciding their "
         u"receivers."
)

translations.define("FormBlock.email_messages",
    ca = u"Notificacions per correu electrònic",
    es = u"Notificaciones por correo electrónico",
    en = u"E-mail notifications"
)

translations.define("FormBlock.redirection",
    ca = u"Redirecció",
    es = u"Redirección",
    en = u"Redirection"
)

translations.define("FormBlock.redirection-explanation",
    ca = u"Deixar en blanc per redirigir a la primera pàgina filla",
    es = u"Dejar en blanco para redirigr a la primera página hija",
    en = u"Leave blank to redirect to the first child page"
)

translations.define("FormBlock.submit_code",
    ca = u"Codi a executar quan s'envii el formulari",
    es = u"Código a ejecutar cuando se envíe el formulario",
    en = u"Code to execute when the form is submitted"
)

translations.define("FormBlock.after_submit_code",
    ca = u"Codi a executar després que s'hagi enviat el formulari",
    es = u"Código a ejecutar después que se haya enviado el formulario",
    en = u"Code to execute after the form has been submitted"
)

translations.define("FormBlock.view_class",
    ca = u"Vista",
    es = u"Vista",
    en = u"View"
)

# Field
#------------------------------------------------------------------------------
translations.define("Field",
    ca = u"Camp",
    es = u"Campo",
    en = u"Field"
)

translations.define("Field-plural",
    ca = u"Camps",
    es = u"Campos",
    en = u"Fields"
)

translations.define("Field.field",
    ca = u"Camp",
    es = u"Campo",
    en = u"Field"
)

translations.define("Field.field_description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("Field.field_structure",
    ca = u"Estructura",
    es = u"Estructura",
    en = u"Structure"
)

translations.define("Field.field_properties",
    ca = u"Propietats",
    es = u"Propiedades",
    en = u"Properties"
)

translations.define("Field.field_name",
    ca = u"Identificador",
    es = u"Identificador",
    en = u"Identifier"
)

translations.define("Field.field_set",
    ca = u"Conjunt",
    es = u"Conjunto",
    en = u"Field set"
)

translations.define("Field.collection",
    ca = u"Col·lecció",
    es = u"Colección",
    en = u"Collection"
)

translations.define("Field.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Field.visible_title",
    ca = u"Nom visible",
    es = u"Nombre visible",
    en = u"Visible name"
)

translations.define("Field.empty_label",
    ca = u"Valor indeterminat",
    es = u"Valor indeterminado",
    en = u"Empty label"
)

translations.define("Field.empty_label-explanation",
    ca = u"El text que es mostrarà quan el camp sigui buit",
    es = u"El texto que se mostrará cuando el campo esté vacío",
    en = u"The text for the field's empty option"
)

translations.define("Field.explanation",
    ca = u"Explicació",
    es = u"Explicación",
    en = u"Explanation"
)

translations.define("Field.is_required_field",
    ca = u"Requerit",
    es = u"Requerido",
    en = u"Required"
)

translations.define("Field.field_edit_control",
    ca = u"Interfície d'usuari",
    es = u"Interfaz de usuario",
    en = u"User interface"
)

translations.define(
    "Field.field_edit_control=none",
    ca = u"Control per defecte",
    es = u"Control por defecto",
    en = u"Default control"
)

translations.define("Field.field_edit_control=cocktail.html.TextBox",
    ca = u"Caixa de text",
    es = u"Caja de texto",
    en = u"Text box"
)

translations.define("Field.field_edit_control=cocktail.html.TextArea",
    ca = u"Caixa de text multilínia",
    es = u"Caja de texto multilinea",
    en = u"Text area"
)

translations.define("Field.field_edit_control=cocktail.html.DropdownSelector",
    ca = u"Selector desplegable",
    es = u"Selector desplegable",
    en = u"Dropdown selector"
)

translations.define("Field.field_edit_control=cocktail.html.RadioSelector",
    ca = u"Botons de radio",
    es = u"Botones de radio",
    en = u"Radio buttons"
)

translations.define("Field.field_edit_control=cocktail.html.CheckBox",
    ca = u"Xec",
    es = u"Check",
    en = u"Check box"
)

translations.define("Field.field_edit_control=cocktail.html.CheckList",
    ca = u"Llista de xecs",
    es = u"Lista de checks",
    en = u"Check list"
)

translations.define("Field.field_edit_control=cocktail.html.DatePicker",
    ca = u"Calendari desplegable",
    es = u"Calendario desplegable",
    en = u"Dropdown calendar"
)

translations.define(
    "Field.field_edit_control=cocktail.html.CompoundDateSelector",
    ca = u"Desplegables separats per dia, mes i any",
    es = u"Desplegables separados para día, mes y año",
    en = u"Separate dropdown selectors for day, month and year"
)

translations.define("Field.field_initialization",
    ca = u"Inicialització",
    es = u"Inicialización",
    en = u"Initialization"
)

# FieldSet
#------------------------------------------------------------------------------
translations.define("FieldSet",
    ca = u"Conjunt de camps",
    es = u"Conjunto de campos",
    en = u"Field set"
)

translations.define("FieldSet-plural",
    ca = u"Conjunts de camps",
    es = u"Conjuntos de campos",
    en = u"Field sets"
)

translations.define("FieldSet.base_field_set",
    ca = u"Base",
    es = u"Base",
    en = u"Base"
)

translations.define("FieldSet.derived_field_sets",
    ca = u"Conjunts derivats",
    es = u"Conjuntos derivados",
    en = u"Derived field sets"
)

translations.define("FieldSet.fields",
    ca = u"Camps",
    es = u"Campos",
    en = u"Fields"
)

# CollectionField
#------------------------------------------------------------------------------
translations.define("CollectionField",
    ca = u"Camp de col·lecció",
    es = u"Campo de colección",
    en = u"Collection field"
)

translations.define("CollectionField-plural",
    ca = u"Camps de col·lecció",
    es = u"Campos de colección",
    en = u"Collection fields"
)

translations.define("CollectionField.items",
    ca = u"Elements de la col·lecció",
    es = u"Elementos de la colección",
    en = u"Collection items"
)

translations.define("CollectionField.min",
    ca = u"Nombre mínim d'elements",
    es = u"Número mínimo de elementos",
    en = u"Minimum number of items"
)

translations.define("CollectionField.max",
    ca = u"Nombre màxim d'elements",
    es = u"Número máximo de elementos",
    en = u"Maximum number of items"
)

# BooleanField
#------------------------------------------------------------------------------
translations.define("BooleanField",
    ca = u"Camp de sí / no",
    es = u"Campo de sí / no",
    en = u"Yes / no field"
)

translations.define("BooleanField-plural",
    ca = u"Camps de sí / no",
    es = u"Campos de sí / no",
    en = u"Yes / no fields"
)

# TextField
#------------------------------------------------------------------------------
translations.define("TextField",
    ca = u"Camp de text",
    es = u"Campo de texto",
    en = u"Text field"
)

translations.define("TextField-plural",
    ca = u"Camps de text",
    es = u"Campos de texto",
    en = u"Text fields"
)

translations.define("TextField.format",
    ca = u"Format",
    es = u"Formato",
    en = u"Format"
)

translations.define("TextField.min",
    ca = u"Longitud mínima",
    es = u"Longitud mínima",
    en = u"Minimum length"
)

translations.define("TextField.max",
    ca = u"Longitud màxima",
    es = u"Longitud máxima",
    en = u"Maximum length"
)

# OptionsField
#------------------------------------------------------------------------------
translations.define("OptionsField",
    ca = u"Camp d'opcions",
    es = u"Campo de opciones",
    en = u"Options field"
)

translations.define("OptionsField-plural",
    ca = u"Camps d'opcions",
    es = u"Campos de opciones",
    en = u"Option fields"
)

translations.define("OptionsField.options",
    ca = u"Opcions",
    es = u"Opciones",
    en = u"Options"
)

# OptionsFieldOption
#------------------------------------------------------------------------------
translations.define("OptionsFieldOption",
    ca = u"Entrada de camp d'opcions",
    es = u"Entrada de campo de opciones",
    en = u"Options field entry"
)

translations.define("OptionsFieldOption-plural",
    ca = u"Entrades de camp d'opcions",
    es = u"Entradas de campo de opciones",
    en = u"Options field entries"
)

translations.define("OptionsFieldOption.field",
    ca = u"Camp",
    es = u"Campo",
    en = u"Name"
)

translations.define("OptionsFieldOption.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("OptionsFieldOption.enabled",
    ca = u"Visible",
    es = u"Visible",
    en = u"Enabled"
)

# EmailAddressField
#------------------------------------------------------------------------------
translations.define("EmailAddressField",
    ca = u"Camp d'adreça de correu electrònic",
    es = u"Campo de dirección de correo electrónico",
    en = u"E-mail address field"
)

translations.define("EmailAddressField-plural",
    ca = u"Camps d'adreça de correu electrònic",
    es = u"Campos de dirección de correo electrónico",
    en = u"E-mail address fields"
)

# PhoneNumberField
#------------------------------------------------------------------------------
translations.define("PhoneNumberField",
    ca = u"Camp de número de telèfon",
    es = u"Campo de número de teléfono",
    en = u"Phone number field"
)

translations.define("PhoneNumberField-plural",
    ca = u"Camps de número de telèfon",
    es = u"Campos de número de teléfono",
    en = u"Phone number fields"
)

# HTMLField
#------------------------------------------------------------------------------
translations.define("HTMLField",
    ca = u"Camp de text enriquit",
    es = u"Campo de texto enriquecido",
    en = u"Rich text field"
)

translations.define("HTMLField-plural",
    ca = u"Camps de text enriquit",
    es = u"Campos de texto enriquecido",
    en = u"Rich text fields"
)

# NumericField
#------------------------------------------------------------------------------
translations.define("NumericField",
    ca = u"Camp numèric",
    es = u"Campo numérico",
    en = u"Numeric field"
)

translations.define("NumericField-plural",
    ca = u"Camps numèrics",
    es = u"Campos numéricos",
    en = u"Numeric fields"
)

translations.define("NumericField.min",
    ca = u"Mínim",
    es = u"Mínimo",
    en = u"Minimum"
)

translations.define("NumericField.max",
    ca = u"Màxim",
    es = u"Máximo",
    en = u"Maximum"
)

# IntegerField
#------------------------------------------------------------------------------
translations.define("IntegerField",
    ca = u"Camp enter",
    es = u"Campo entero",
    en = u"Integer field"
)

translations.define("IntegerField-plural",
    ca = u"Camps enters",
    es = u"Campos enteros",
    en = u"Integer fields"
)

# DecimalField
#------------------------------------------------------------------------------
translations.define("DecimalField",
    ca = u"Camp decimal",
    es = u"Campo decimal",
    en = u"Decimal field"
)

translations.define("DecimalField-plural",
    ca = u"Camps decimals",
    es = u"Campos decimales",
    en = u"Decimal fields"
)

# DateField
#------------------------------------------------------------------------------
translations.define("DateField",
    ca = u"Camp de data",
    es = u"Campo de fecha",
    en = u"Date field"
)

translations.define("DateField-plural",
    ca = u"Camps de data",
    es = u"Campos de fecha",
    en = u"Date fields"
)

# TimeField
#------------------------------------------------------------------------------
translations.define("TimeField",
    ca = u"Camp d'hora",
    es = u"Campo de hora",
    en = u"Time field"
)

translations.define("TimeField-plural",
    ca = u"Camps d'hora",
    es = u"Campos de hora",
    en = u"Time fields"
)

# DateTimeField
#------------------------------------------------------------------------------
translations.define("DateTimeField",
    ca = u"Camp de data / hora",
    es = u"Campo de fecha / hora",
    en = u"Date / time field"
)

translations.define("DateTimeField-plural",
    ca = u"Camps de data / hora",
    es = u"Campos de fecha / hora",
    en = u"Date / time fields"
)

# FormAgreement
#------------------------------------------------------------------------------
translations.define("FormAgreement",
    ca = u"Termes i condicions",
    es = u"Términos y condiciones",
    en = u"Terms and conditions"
)

translations.define("FormAgreement-plural",
    ca = u"Termes i condicions",
    es = u"Términos y condiciones",
    en = u"Terms and conditions"
)

translations.define("FormAgreement.forms",
    ca = u"Formularis",
    es = u"Formularios",
    en = u"Forms"
)

translations.define("FormAgreement.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("FormAgreement.document",
    ca = u"Document",
    es = u"Documento",
    en = u"Document"
)

