#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from cocktail.translations import translations

for cls_name in ("Configuration", "Website"):
    translations.define(cls_name + ".external_files_host",
        ca = u"Domini fitxers externs",
        es = u"Dominio ficheros externos",
        en = u"External files host"
    )

