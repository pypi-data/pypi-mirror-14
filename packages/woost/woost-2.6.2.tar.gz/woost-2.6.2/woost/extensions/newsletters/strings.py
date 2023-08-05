#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

# Installation
#------------------------------------------------------------------------------
translations.define("woost.extensions.newsletters.newsletter_controller.title",
    ca = u"Controlador de butlletins",
    es = u"Controlador de boletines",
    en = u"Newsletter controller"
)

translations.define("woost.extensions.newsletters.newsletter_template.title",
    ca = u"Plantilla de butlletí",
    es = u"Plantilla de boletín",
    en = u"Newsletter template"
)

translations.define("woost.extensions.newsletters.image_factories.third.title",
    ca = u"Butlletí - 33%",
    es = u"Boletín - 33%",
    en = u"Newsletter - 33%"
)

translations.define("woost.extensions.newsletters.image_factories.half.title",
    ca = u"Butlletí - 50%",
    es = u"Boletín - 50%",
    en = u"Newsletter - 50%"
)

translations.define(
    "woost.extensions.newsletters.image_factories.full.title",
    ca = u"Butlletí - 100%",
    es = u"Boletín - 100%",
    en = u"Newsletter - 100%"
)

# ImageFactory
#------------------------------------------------------------------------------
translations.define("ImageFactory.applicable_to_newsletters",
    ca = u"Aplicable a butlletins de notícies",
    es = u"Aplicable a boletines de noticias",
    en = u"Applicable to newsletters"
)

# Newsletter
#------------------------------------------------------------------------------
translations.define("Newsletter",
    ca = u"Butlletí de notícies",
    es = u"Boletín de noticias",
    en = u"Newsletter"
)

translations.define("Newsletter-plural",
    ca = u"Butlletins de notícies",
    es = u"Boletines de noticias",
    en = u"Newsletters"
)

translations.define("Newsletter.blocks",
    ca = u"Blocs",
    es = u"Bloques",
    en = u"Blocks"
)

# NewsletterContent
#------------------------------------------------------------------------------
translations.define("NewsletterContent",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("NewsletterContent-plural",
    ca = u"Continguts",
    es = u"Contenidos",
    en = u"Content"
)

translations.define("NewsletterContent.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "NewsletterContent.view_class"
    "=woost.extensions.newsletters.NewsletterContentView",
    ca = u"Estàndard",
    es = u"Estándar",
    en = u"Standard"
)

translations.define("NewsletterContent.text",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define("NewsletterContent.image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define("NewsletterContent.image_alignment",
    ca = u"Alineament",
    es = u"Alineamiento",
    en = u"Alignment"
)

translations.define("NewsletterContent.image_alignment=image_left",
    ca = u"Imatge a l'esquerra",
    es = u"Imagen a la izquierda",
    en = u"Image left"
)

translations.define("NewsletterContent.image_alignment=image_right",
    ca = u"Imatge a la dreta",
    es = u"Imagen a la derecha",
    en = u"Image right"
)

translations.define("NewsletterContent.image_alignment=image_top",
    ca = u"Imatge a dalt",
    es = u"Imagen arriba",
    en = u"Image top"
)

translations.define("NewsletterContent.image_factory",
    ca = u"Processat d'imatge",
    es = u"Procesado de imagen",
    en = u"Image processing"
)

translations.define("NewsletterContent.link",
    ca = u"Enllaç",
    es = u"Enlace",
    en = u"Link"
)

# NewsletterBox
#------------------------------------------------------------------------------
translations.define("NewsletterBox",
    ca = u"Caixa",
    es = u"Caja",
    en = u"Box"
)

translations.define("NewsletterBox-plural",
    ca = u"Caixes",
    es = u"Cajas",
    en = u"Boxes"
)

translations.define("NewsletterBox.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "NewsletterBox.view_class"
    "=woost.extensions.newsletters.NewsletterBoxView",
    ca = u"Estàndard",
    es = u"Estándar",
    en = u"Standard"
)

translations.define("NewsletterBox.blocks",
    ca = u"Blocs",
    es = u"Bloques",
    en = u"Blocks"
)

# NewsletterListing
#------------------------------------------------------------------------------
translations.define("NewsletterListing",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("NewsletterListing-plural",
    ca = u"Llistats",
    es = u"Listados",
    en = u"Listings"
)

translations.define("NewsletterListing.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "NewsletterListing.view_class"
    "=woost.extensions.newsletters.NewsletterListingTextOnlyView",
    ca = u"Només text",
    es = u"Solo texto",
    en = u"Text only"
)

translations.define(
    "NewsletterListing.view_class"
    "=woost.extensions.newsletters.NewsletterListingTextAndIconView",
    ca = u"Text i icona",
    es = u"Texto e icono",
    en = u"Text and icon"
)

translations.define(
    "NewsletterListing.view_class"
    "=woost.extensions.newsletters.NewsletterListingSummaryView",
    ca = u"Resum",
    es = u"Resumen",
    en = u"Summary"
)

translations.define("NewsletterListing.listed_items",
    ca = u"Elements a llistar",
    es = u"Elementos a listar",
    en = u"Listed items"
)

