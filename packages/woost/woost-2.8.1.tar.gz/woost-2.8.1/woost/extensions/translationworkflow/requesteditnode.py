#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import cached_getter
from cocktail import schema
from cocktail.html.uigeneration import display_factory
from woost.controllers.backoffice.editstack import EditNode


class TranslationWorkflowRequestEditNode(EditNode):

    translated_values_key = "translated_values"

    @cached_getter
    def form_schema(self):
        form_schema = EditNode.form_schema(self)

        # Show the changelog for the request and its source item
        form_schema.add_member(
            schema.Member(
                "translation_workflow_changelog",
                editable = schema.READ_ONLY,
                member_group = "translation_request.changelog",
                backoffice_display = display_factory(
                    "woost.views.ChangeLog",
                    changes = [
                        change
                        for change in (
                              list(self.item.changes)
                            + list(self.item.translated_item.changes)
                        )
                        if change.is_explicit_change
                    ],
                    language_subset = (
                        self.item.source_language,
                        self.item.target_language
                    ),
                    exclude_member = lambda member:
                        member.name == "translation_requests",
                    show_all_changes = False
                )
            )
        )

        return form_schema

    @cached_getter
    def form_adapter(self):
        adapter = EditNode.form_adapter(self)

        editable = self.get_member_edit_mode(
            self.item.__class__.translated_values
        )
        if editable == schema.EDITABLE:
            adapter.export_rules.add_rule(
                TranslatedValuesExportRule(self.item),
                position = 0
            )
            adapter.import_rules.add_rule(
                TranslatedValuesImportRule(self.item),
                position = 0
            )
        return adapter


class TranslatedValuesRule(schema.Rule):

    key = "translated_values"

    def __init__(self, request):
        schema.Rule.__init__(self)
        self.request = request

    @cached_getter
    def translation_map(self):
        return dict(
            (member.name, self.key + "_" + member.name)
            for member in self.request.translated_item.__class__.iter_members()
            if member.translated and member.included_in_translation_workflow
        )


class TranslatedValuesExportRule(TranslatedValuesRule):

    @cached_getter
    def translated_values_adapter(self):
        adapter = schema.Adapter()
        adapter.implicit_copy = False
        adapter.copy(self.translation_map, properties = {
            "required": False,
            "translated": False,
            "unique": False,
            "member_group": "translation_request.translated_values"
        })
        return adapter

    def adapt_schema(self, context):
        if context.consume(self.key):

            # Preserve the 'original_member' and 'source_member' properties
            original_member = context.target_schema.original_member
            source_member = context.target_schema.source_member

            self.translated_values_adapter.export_schema(
                self.request.translated_item.__class__,
                context.target_schema
            )

            context.target_schema.original_member = original_member
            context.target_schema.source_member = source_member

    def adapt_object(self, context):
        if context.consume(self.key):
            item = self.request.translated_item
            values = self.request.translated_values
            for orig_key, trans_key in self.translation_map.iteritems():
                try:
                    value = values.get(orig_key)
                except AttributeError, KeyError:
                    value = item.get(orig_key, self.request.target_language)
                context.set(trans_key, value)


class TranslatedValuesImportRule(TranslatedValuesRule):

    def adapt_object(self, context):
        context.consume(self.key)
        values = self.request.translated_values
        if values is None:
            self.request.translated_values = values = {}
        for orig_key, trans_key in self.translation_map.iteritems():
            if context.consume(trans_key):
                values[orig_key] = context.get(trans_key)

