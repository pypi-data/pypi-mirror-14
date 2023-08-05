#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations

translations.define("woost.extensions.annotations.Annotation-instance",
    ca = lambda instance, **kwargs:
        translations(instance.annotation_target, **kwargs) + u" (notes)",
    es = lambda instance, **kwargs:
        translations(instance.annotation_target, **kwargs) + u" (notas)",
    en = lambda instance, **kwargs:
        translations(instance.annotation_target, **kwargs) + u" (notes)"
)

translations.define(
    "woost.extensions.annotations.FormOverlay.annotationDropdown.label",
    ca = u"Annotacions per aquest camp",
    es = u"Anotaciones para este campo",
    en = u"Annotations for this field"
)

