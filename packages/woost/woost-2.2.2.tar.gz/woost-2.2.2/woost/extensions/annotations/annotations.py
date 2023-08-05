#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.schema.exceptions import SchemaIntegrityError
from cocktail.translations import translations

schema.Member._special_copy_keys.add("_annotation")
_base_deep_copy = schema.Member.__deepcopy__

def _deep_copy(self, memo):
    copy = _base_deep_copy(self, memo)
    copy._annotation = self._annotation
    return copy

schema.Member.__deepcopy__ = _deep_copy

schema.Member._annotation = None

def _get_annotation(self):
    return self._annotation

schema.Member.annotation = property(_get_annotation)

def add_annotation(self, **kwargs):

    if self._annotation:
        return self._annotation

    if isinstance(self, Annotation):
        raise SchemaIntegrityError(
            "Can't annotate an annotation member"
        )

    if not self.name:
        raise SchemaIntegrityError(
            "Can't annotate an anonymous member"
        )

    if not self.schema:
        raise SchemaIntegrityError(
            "Can't annotate a member that doesn't belong to a schema"
        )

    annotation = Annotation(self.name + "_annotation", **kwargs)
    annotation._annotation_target = self
    self._annotation = annotation
    annotation.translated = self.translated
    self.schema.add_member(annotation)
    return annotation

schema.Member.add_annotation = add_annotation


class Annotation(schema.String):

    _annotation_target = None
    listed_by_default = False
    edit_control = "cocktail.html.TextArea"

    def __translate__(self, language, **kwargs):
        return translations(
            "woost.extensions.annotations.Annotation-instance",
            instance = self,
            language = language,
            **kwargs
        )

    _special_copy_keys = set(schema.String._special_copy_keys)
    _special_copy_keys.add("_annotation_target")

    def __deepcopy__(self, memo):
        copy = schema.String.__deepcopy__(self, memo)
        copy._annotation_target = self._annotation_target
        return copy

    @property
    def annotation_target(self):
        return self._annotation_target

    @property
    def after_member(self):
        return self._annotation_target.name

    @property
    def member_group(self):
        return self._annotation_target.member_group

